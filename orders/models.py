import random
import string
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from core.models import BaseModel
from users.models import User, Address
from products.models import Product


def generate_order_number():
    return "ORD-" + "".join(random.choices(string.digits, k=10))


class Order(BaseModel):
    """
    Order header. Financial amounts are stored as snapshots at order time
    (not recalculated from live Product prices later) — required so order
    history remains accurate even after a product's price changes.
    """

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        AWAITING_PRESCRIPTION = "AWAITING_PRESCRIPTION", "Awaiting Prescription Approval"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PROCESSING = "PROCESSING", "Processing"
        SHIPPED = "SHIPPED", "Shipped"
        OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for Delivery"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"
        REFUNDED = "REFUNDED", "Refunded"
        RETURNED = "RETURNED", "Returned"

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"
        PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED", "Partially Refunded"

    order_number = models.CharField(
        max_length=20, unique=True, default=generate_order_number, db_index=True
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")

    status = models.CharField(
        max_length=25, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING,
        db_index=True
    )

    # Snapshotted addresses (FK kept for reference, but key fields duplicated
    # below in case the Address record is later edited or deleted)
    shipping_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="shipping_orders"
    )
    billing_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="billing_orders"
    )
    shipping_address_snapshot = models.JSONField(default=dict)
    billing_address_snapshot = models.JSONField(default=dict)

    # Financials
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])

    coupon_code = models.CharField(max_length=50, blank=True)

    # Prescription gating
    requires_prescription_verification = models.BooleanField(default=False)
    prescription = models.ForeignKey(
        "prescriptions.Prescription", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="orders"
    )

    customer_notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True, help_text="Admin/staff only")

    tracking_number = models.CharField(max_length=100, blank=True)
    courier_name = models.CharField(max_length=100, blank=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["order_number"]),
            models.Index(fields=["payment_status"]),
        ]

    def __str__(self):
        return f"{self.order_number} - {self.user} - {self.status}"


class OrderItem(BaseModel):
    """
    Line item with price/name snapshotted at purchase time — order history
    must remain immutable and accurate regardless of later catalog changes.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="order_items"
    )
    product_name_snapshot = models.CharField(max_length=255)
    product_sku_snapshot = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
    required_prescription = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.product_name_snapshot}"


class OrderStatusHistory(BaseModel):
    """Append-only log of every status transition — powers the customer-facing
    order tracking timeline and admin audit trail."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    status = models.CharField(max_length=25, choices=Order.Status.choices)
    note = models.CharField(max_length=500, blank=True)
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="order_status_changes"
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "Order status histories"

    def __str__(self):
        return f"{self.order.order_number} -> {self.status}"
