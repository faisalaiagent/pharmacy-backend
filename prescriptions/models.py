from django.db import models

from core.models import BaseModel
from users.models import User


class Prescription(BaseModel):
    """
    A customer-uploaded prescription. One Prescription can cover multiple
    line items (PrescriptionItem) since a doctor's prescription typically
    lists several medicines. Status is tracked at the prescription level;
    PrescriptionReview stores the immutable audit trail of pharmacist
    decisions, since a prescription can be resubmitted/re-reviewed.
    """

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending Review"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        EXPIRED = "EXPIRED", "Expired"

    class FileType(models.TextChoices):
        IMAGE = "IMAGE", "Image"
        PDF = "PDF", "PDF"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prescriptions")
    file_url = models.URLField(help_text="Cloudinary/S3 secure URL")
    file_type = models.CharField(max_length=10, choices=FileType.choices)
    file_size_bytes = models.PositiveIntegerField(default=0)

    patient_name = models.CharField(
        max_length=255, blank=True,
        help_text="Name on prescription, may differ from account holder"
    )
    doctor_name = models.CharField(max_length=255, blank=True)
    doctor_license_number = models.CharField(max_length=100, blank=True)
    issued_date = models.DateField(null=True, blank=True)

    customer_notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True
    )

    assigned_pharmacist = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="assigned_prescriptions",
        limit_choices_to={"role": "PHARMACIST"}
    )

    # Secure storage / access control
    access_token = models.CharField(
        max_length=64, blank=True,
        help_text="Time-limited token for secure pharmacist viewing link"
    )
    valid_until = models.DateField(
        null=True, blank=True,
        help_text="Prescription validity expiry per regulatory requirement"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["assigned_pharmacist", "status"]),
        ]

    def __str__(self):
        return f"Prescription #{str(self.id)[:8]} - {self.user} - {self.status}"


class PrescriptionItem(BaseModel):
    """Individual medicine line-item parsed/declared from a prescription,
    optionally linked to a catalog Product once matched."""
    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="prescription_items"
    )
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    instructions = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.medicine_name} x{self.quantity}"


class PrescriptionReview(BaseModel):
    """
    Immutable audit record of each pharmacist decision on a prescription.
    A prescription may be reviewed more than once (e.g. resubmission after
    rejection), so this is append-only history rather than a field on
    Prescription itself — required for regulatory audit trails.
    """

    class Decision(models.TextChoices):
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        NEEDS_CLARIFICATION = "NEEDS_CLARIFICATION", "Needs Clarification"

    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name="reviews"
    )
    pharmacist = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name="prescription_reviews",
        limit_choices_to={"role": "PHARMACIST"}
    )
    decision = models.CharField(max_length=25, choices=Decision.choices)
    comments = models.TextField(blank=True)
    rejection_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["prescription", "-created_at"])]

    def __str__(self):
        return f"{self.decision} by {self.pharmacist} on {self.prescription}"
