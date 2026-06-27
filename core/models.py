import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model providing UUID primary key and audit timestamps.
    All domain models inherit from this for consistency and to avoid
    sequential-integer ID enumeration attacks on a public-facing pharmacy API.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(BaseModel):
    """
    Abstract base model for entities that must be soft-deleted rather than
    physically removed (e.g. Products, Orders) — required for audit trails,
    regulatory record-keeping, and order history integrity even after a
    product is discontinued or a user is deactivated.
    """
    is_active = models.BooleanField(default=True, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        from django.utils import timezone
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_active", "deleted_at"])


class AuditLog(BaseModel):
    """
    System-wide audit trail. Required for pharmaceutical compliance —
    tracks who did what, when, to which record. Critical for prescription
    approvals/rejections, inventory adjustments, and order status changes.
    """
    ACTION_CHOICES = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("APPROVE", "Approve"),
        ("REJECT", "Reject"),
        ("LOGIN", "Login"),
        ("LOGIN_FAILED", "Login Failed"),
        ("STATUS_CHANGE", "Status Change"),
    ]

    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="audit_logs"
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, db_index=True)
    model_name = models.CharField(max_length=100, db_index=True)
    object_id = models.CharField(max_length=64, db_index=True)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["model_name", "object_id"]),
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.action} on {self.model_name}({self.object_id}) by {self.user}"
