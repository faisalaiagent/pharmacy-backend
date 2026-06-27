import logging
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from core.permissions import IsAdmin, IsOwnerOrAdmin
from core.responses import success_response, error_response, created_response, EnvelopeMixin
from core.pagination import StandardPagination
from cart_wishlist.models import Cart, CartItem
from coupons.models import Coupon, CouponUsage
from products.models import Product
from users.models import Address
from .models import Order, OrderItem, OrderStatusHistory
from .serializers import OrderSerializer, PlaceOrderSerializer, UpdateOrderStatusSerializer

logger = logging.getLogger(__name__)


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=PlaceOrderSerializer, tags=["Orders"])
    def post(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Order validation failed.", serializer.errors)

        data = serializer.validated_data
        user = request.user

        # Validate shipping address belongs to user
        try:
            shipping_address = Address.objects.get(id=data["shipping_address_id"], user=user)
        except Address.DoesNotExist:
            return error_response("Shipping address not found.")

        billing_address = shipping_address
        if data.get("billing_address_id"):
            try:
                billing_address = Address.objects.get(id=data["billing_address_id"], user=user)
            except Address.DoesNotExist:
                return error_response("Billing address not found.")

        # Load cart
        try:
            cart = Cart.objects.prefetch_related("items__product").get(user=user)
        except Cart.DoesNotExist:
            return error_response("Your cart is empty.")

        cart_items = list(cart.items.all())
        if not cart_items:
            return error_response("Your cart is empty.")

        # Check prescription requirement
        needs_prescription = any(item.product.requires_prescription for item in cart_items)
        prescription = None
        if needs_prescription:
            if not data.get("prescription_id"):
                return error_response(
                    "One or more items in your cart require a valid prescription. "
                    "Please upload a prescription before placing this order."
                )
            from prescriptions.models import Prescription
            try:
                prescription = Prescription.objects.get(
                    id=data["prescription_id"], user=user, status="APPROVED"
                )
            except Prescription.DoesNotExist:
                return error_response("A valid approved prescription is required.")

        with transaction.atomic():
            # Calculate totals
            subtotal = Decimal("0.00")
            discount_amount = Decimal("0.00")
            shipping_amount = Decimal("0.00")  # flat rate / free — plug in logic here

            for item in cart_items:
                if item.product.stock_quantity < item.quantity:
                    return error_response(
                        f"'{item.product.name}' only has {item.product.stock_quantity} unit(s) left."
                    )
                subtotal += item.product.final_price * item.quantity

            # Coupon validation
            coupon = None
            coupon_code = data.get("coupon_code", "")
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    if not coupon.is_valid():
                        return error_response("Coupon is expired or no longer valid.")
                    if subtotal < coupon.min_order_amount:
                        return error_response(
                            f"Minimum order amount for this coupon is {coupon.min_order_amount}."
                        )
                    user_uses = CouponUsage.objects.filter(coupon=coupon, user=user).count()
                    if user_uses >= coupon.usage_limit_per_user:
                        return error_response("You have already used this coupon.")

                    if coupon.discount_type == "PERCENTAGE":
                        discount_amount = subtotal * (coupon.discount_value / 100)
                        if coupon.max_discount_amount:
                            discount_amount = min(discount_amount, coupon.max_discount_amount)
                    else:
                        discount_amount = min(coupon.discount_value, subtotal)
                except Coupon.DoesNotExist:
                    return error_response("Invalid coupon code.")

            total_amount = subtotal - discount_amount + shipping_amount

            # Create Order
            order_status = (
                Order.Status.AWAITING_PRESCRIPTION if needs_prescription
                else Order.Status.PENDING
            )

            def addr_snapshot(addr):
                return {
                    "full_name": addr.full_name,
                    "phone_number": addr.phone_number,
                    "address_line_1": addr.address_line_1,
                    "address_line_2": addr.address_line_2,
                    "city": addr.city,
                    "state_province": addr.state_province,
                    "postal_code": addr.postal_code,
                    "country": addr.country,
                }

            order = Order.objects.create(
                user=user,
                status=order_status,
                shipping_address=shipping_address,
                billing_address=billing_address,
                shipping_address_snapshot=addr_snapshot(shipping_address),
                billing_address_snapshot=addr_snapshot(billing_address),
                subtotal=subtotal,
                discount_amount=discount_amount,
                shipping_amount=shipping_amount,
                total_amount=total_amount,
                coupon_code=coupon_code,
                requires_prescription_verification=needs_prescription,
                prescription=prescription,
                customer_notes=data.get("customer_notes", ""),
            )

            # Create order items + decrement stock atomically
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name_snapshot=item.product.name,
                    product_sku_snapshot=item.product.sku,
                    unit_price=item.product.final_price,
                    quantity=item.quantity,
                    line_total=item.product.final_price * item.quantity,
                    required_prescription=item.product.requires_prescription,
                )
                Product.objects.filter(id=item.product.id).update(
                    stock_quantity=item.product.stock_quantity - item.quantity
                )

            # Log initial status
            OrderStatusHistory.objects.create(
                order=order, status=order_status, changed_by=user,
                note="Order placed by customer."
            )

            # Mark coupon usage
            if coupon:
                coupon.times_used += 1
                coupon.save(update_fields=["times_used"])
                CouponUsage.objects.create(coupon=coupon, user=user, order=order)

            # Clear cart
            cart.items.all().delete()

        logger.info("Order placed: %s by %s", order.order_number, user.email)
        return created_response(OrderSerializer(order).data, f"Order {order.order_number} placed!")


class OrderListView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    @extend_schema(tags=["Orders"])
    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related("items", "status_history")
            .select_related("shipping_address")
            .order_by("-created_at")
        )


class OrderDetailView(EnvelopeMixin, generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Orders"])
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "items", "status_history"
        )

    def get_object(self):
        obj = super().get_object()
        return obj


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Orders"])
    def post(self, request, order_number):
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
        except Order.DoesNotExist:
            return error_response("Order not found.", status_code=status.HTTP_404_NOT_FOUND)

        cancellable_statuses = [Order.Status.PENDING, Order.Status.AWAITING_PRESCRIPTION]
        if order.status not in cancellable_statuses:
            return error_response(f"Orders with status '{order.status}' cannot be cancelled.")

        with transaction.atomic():
            # Restore stock
            for item in order.items.select_related("product"):
                if item.product:
                    Product.objects.filter(id=item.product.id).update(
                        stock_quantity=item.product.stock_quantity + item.quantity
                    )
            order.status = Order.Status.CANCELLED
            order.cancelled_at = timezone.now()
            order.cancellation_reason = request.data.get("reason", "Cancelled by customer.")
            order.save(update_fields=["status", "cancelled_at", "cancellation_reason"])

            OrderStatusHistory.objects.create(
                order=order, status=Order.Status.CANCELLED,
                changed_by=request.user,
                note=order.cancellation_reason,
            )

        return success_response(OrderSerializer(order).data, "Order cancelled successfully.")


# ── Admin order management ────────────────────────────────────────────────────

class AdminOrderListView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin]
    pagination_class = StandardPagination
    filterset_fields = ["status", "payment_status", "requires_prescription_verification"]
    search_fields = ["order_number", "user__email"]

    @extend_schema(tags=["Admin - Orders"])
    def get_queryset(self):
        return (
            Order.objects.all()
            .prefetch_related("items", "status_history")
            .select_related("user", "shipping_address")
            .order_by("-created_at")
        )


class AdminUpdateOrderStatusView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(request=UpdateOrderStatusSerializer, tags=["Admin - Orders"])
    def patch(self, request, order_number):
        serializer = UpdateOrderStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Invalid data.", serializer.errors)

        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return error_response("Order not found.", status_code=status.HTTP_404_NOT_FOUND)

        new_status = serializer.validated_data["status"]
        order.status = new_status
        if serializer.validated_data.get("tracking_number"):
            order.tracking_number = serializer.validated_data["tracking_number"]
        if serializer.validated_data.get("courier_name"):
            order.courier_name = serializer.validated_data["courier_name"]
        if new_status == Order.Status.DELIVERED:
            order.delivered_at = timezone.now()
        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            changed_by=request.user,
            note=serializer.validated_data.get("note", ""),
        )
        return success_response(OrderSerializer(order).data, f"Order status updated to {new_status}.")
