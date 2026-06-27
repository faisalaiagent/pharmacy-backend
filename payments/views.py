import json
import logging
import stripe
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from core.permissions import IsAdmin
from core.responses import success_response, error_response
from orders.models import Order, OrderStatusHistory
from .models import Payment

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCreatePaymentIntentView(APIView):
    """
    Creates a Stripe PaymentIntent for a given order.
    Frontend receives the client_secret and completes the payment using
    Stripe Elements — card data never touches our server (PCI compliance).
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"])
    def post(self, request):
        order_number = request.data.get("order_number")
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
        except Order.DoesNotExist:
            return error_response("Order not found.", status_code=status.HTTP_404_NOT_FOUND)

        if order.payment_status == Order.PaymentStatus.PAID:
            return error_response("This order has already been paid.")

        # Amount in smallest currency unit (paise/cents)
        amount_cents = int(order.total_amount * 100)

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency="usd",
                metadata={
                    "order_number": order.order_number,
                    "user_id": str(order.user.id),
                },
            )
        except stripe.StripeError as e:
            logger.error("Stripe PaymentIntent creation failed: %s", str(e))
            return error_response("Payment service error. Please try again.")

        # Record a pending Payment object
        Payment.objects.update_or_create(
            order=order,
            method=Payment.Method.STRIPE,
            defaults={
                "status": Payment.Status.PENDING,
                "amount": order.total_amount,
                "gateway_payment_intent_id": intent.id,
            }
        )

        return success_response({
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
            "amount": str(order.total_amount),
            "currency": "USD",
        }, "Payment intent created.")


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    """
    Stripe sends events here after payment completes/fails.
    CSRF exempt because Stripe signs events with STRIPE_WEBHOOK_SECRET instead.
    """
    permission_classes = [AllowAny]

    @extend_schema(exclude=True)  # Don't expose in Swagger
    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.SignatureVerificationError) as e:
            logger.warning("Stripe webhook signature verification failed: %s", str(e))
            return error_response("Invalid signature.", status_code=status.HTTP_400_BAD_REQUEST)

        event_type = event["type"]
        intent = event["data"]["object"]

        order_number = intent.get("metadata", {}).get("order_number")
        if not order_number:
            return success_response(message="No order reference in event.")

        try:
            order = Order.objects.get(order_number=order_number)
            payment = Payment.objects.filter(
                order=order, gateway_payment_intent_id=intent["id"]
            ).first()
        except Order.DoesNotExist:
            logger.error("Stripe webhook: order %s not found", order_number)
            return success_response()  # Return 200 so Stripe doesn't retry

        if event_type == "payment_intent.succeeded":
            if payment:
                payment.status = Payment.Status.COMPLETED
                payment.paid_at = timezone.now()
                payment.gateway_response = dict(intent)
                payment.save()

            order.payment_status = Order.PaymentStatus.PAID
            order.status = Order.Status.CONFIRMED
            order.save(update_fields=["payment_status", "status"])

            OrderStatusHistory.objects.create(
                order=order, status=Order.Status.CONFIRMED,
                note="Payment confirmed via Stripe."
            )
            logger.info("Payment succeeded for order %s", order_number)

        elif event_type == "payment_intent.payment_failed":
            if payment:
                payment.status = Payment.Status.FAILED
                payment.failure_reason = intent.get("last_payment_error", {}).get("message", "")
                payment.save()

            order.payment_status = Order.PaymentStatus.FAILED
            order.save(update_fields=["payment_status"])
            logger.warning("Payment failed for order %s", order_number)

        return success_response(message="Webhook processed.")


class CODConfirmView(APIView):
    """Marks a COD order as confirmed (payment will be collected on delivery)."""
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"])
    def post(self, request):
        order_number = request.data.get("order_number")
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
        except Order.DoesNotExist:
            return error_response("Order not found.", status_code=status.HTTP_404_NOT_FOUND)

        Payment.objects.create(
            order=order,
            method=Payment.Method.COD,
            status=Payment.Status.PENDING,
            amount=order.total_amount,
        )

        order.status = Order.Status.CONFIRMED
        order.payment_status = Order.PaymentStatus.PENDING
        order.save(update_fields=["status", "payment_status"])

        OrderStatusHistory.objects.create(
            order=order, status=Order.Status.CONFIRMED,
            changed_by=request.user,
            note="Cash on Delivery order confirmed."
        )

        return success_response(message=f"Order {order.order_number} confirmed. Pay on delivery.")


class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"])
    def get(self, request):
        from payments.models import Payment as PaymentModel
        from rest_framework import serializers as drf_serializers

        class PaymentSerializer(drf_serializers.ModelSerializer):
            order_number = drf_serializers.CharField(source="order.order_number")

            class Meta:
                model = PaymentModel
                fields = ("id", "order_number", "method", "status", "amount",
                          "currency", "paid_at", "created_at")

        payments = PaymentModel.objects.filter(
            order__user=request.user
        ).select_related("order").order_by("-created_at")

        return success_response(PaymentSerializer(payments, many=True).data)
