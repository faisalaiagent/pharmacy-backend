from django.db import models

from core.models import BaseModel
from users.models import User


class Notification(BaseModel):
    class NotificationType(models.TextChoices):
        ORDER_PLACED = "ORDER_PLACED", "Order Placed"
        ORDER_STATUS_CHANGED = "ORDER_STATUS_CHANGED", "Order Status Changed"
        PRESCRIPTION_APPROVED = "PRESCRIPTION_APPROVED", "Prescription Approved"
        PRESCRIPTION_REJECTED = "PRESCRIPTION_REJECTED", "Prescription Rejected"
        PAYMENT_RECEIVED = "PAYMENT_RECEIVED", "Payment Received"
        PAYMENT_FAILED = "PAYMENT_FAILED", "Payment Failed"
        LOW_STOCK_ALERT = "LOW_STOCK_ALERT", "Low Stock Alert"
        ACCOUNT = "ACCOUNT", "Account"
        PROMOTIONAL = "PROMOTIONAL", "Promotional"
        SYSTEM = "SYSTEM", "System"

    class Channel(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"
        IN_APP = "IN_APP", "In-App"
        PUSH = "PUSH", "Push"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True
    )
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices, db_index=True)
    channel = models.CharField(max_length=10, choices=Channel.choices, default=Channel.IN_APP)
    title = models.CharField(max_length=255)
    message = models.TextField()
    link_url = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    # For admin-targeted alerts not tied to a specific user (e.g. low stock,
    # new prescription needing review)
    is_admin_alert = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["is_admin_alert", "is_read"]),
        ]

    def __str__(self):
        return f"{self.notification_type} -> {self.user or 'ADMIN'}"
