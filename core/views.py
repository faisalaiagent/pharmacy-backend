from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from core.permissions import IsAdmin
from core.responses import success_response
from orders.models import Order
from users.models import User
from products.models import Product
from prescriptions.models import Prescription
from payments.models import Payment


class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(tags=["Admin - Analytics"])
    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        seven_days_ago = now - timedelta(days=7)

        total_revenue = Payment.objects.filter(
            status="COMPLETED"
        ).aggregate(total=Sum("amount"))["total"] or 0

        revenue_30d = Payment.objects.filter(
            status="COMPLETED", created_at__gte=thirty_days_ago
        ).aggregate(total=Sum("amount"))["total"] or 0

        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status="PENDING").count()
        orders_7d = Order.objects.filter(created_at__gte=seven_days_ago).count()

        total_users = User.objects.filter(role="CUSTOMER").count()
        new_users_30d = User.objects.filter(
            role="CUSTOMER", created_at__gte=thirty_days_ago
        ).count()

        total_products = Product.objects.filter(is_active=True).count()
        low_stock_count = Product.objects.filter(is_active=True, stock_status="LOW_STOCK").count()
        out_of_stock_count = Product.objects.filter(is_active=True, stock_status="OUT_OF_STOCK").count()

        pending_prescriptions = Prescription.objects.filter(status="PENDING").count()
        under_review_prescriptions = Prescription.objects.filter(status="UNDER_REVIEW").count()

        order_status_breakdown = list(
            Order.objects.values("status").annotate(count=Count("id"))
        )

        from orders.models import OrderItem
        top_products = list(
            OrderItem.objects.filter(order__status="DELIVERED")
            .values("product_name_snapshot")
            .annotate(total_sold=Sum("quantity"))
            .order_by("-total_sold")[:5]
        )

        return success_response({
            "revenue": {
                "total": float(total_revenue),
                "last_30_days": float(revenue_30d),
            },
            "orders": {
                "total": total_orders,
                "pending": pending_orders,
                "last_7_days": orders_7d,
                "status_breakdown": order_status_breakdown,
            },
            "users": {
                "total_customers": total_users,
                "new_last_30_days": new_users_30d,
            },
            "products": {
                "total_active": total_products,
                "low_stock": low_stock_count,
                "out_of_stock": out_of_stock_count,
            },
            "prescriptions": {
                "pending_review": pending_prescriptions,
                "under_review": under_review_prescriptions,
            },
            "top_products": top_products,
        })
