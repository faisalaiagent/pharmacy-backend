import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from core.models import BaseModel


class User(AbstractUser):
    """
    Custom user model. Email is the primary login identifier (not username),
    which is the standard expectation for an e-commerce platform.

    Role drives RBAC across the entire platform — every permission class in
    every app checks `request.user.role` rather than relying solely on
    Django's built-in groups, since the role set here is small, fixed, and
    domain-specific (Customer / Pharmacist / Admin).
    """

    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        PHARMACIST = "PHARMACIST", "Pharmacist"
        ADMIN = "ADMIN", "Admin"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.CUSTOMER, db_index=True
    )

    phone_regex = RegexValidator(
        regex=r"^\+?[0-9]{7,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, db_index=True
    )
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.URLField(blank=True, help_text="Cloudinary URL")

    # Account security / audit fields
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    # Marketing / notification preferences
    accepts_marketing_emails = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        indexes = [
            models.Index(fields=["role", "is_active"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    @property
    def is_locked(self):
        from django.utils import timezone
        return bool(self.locked_until and self.locked_until > timezone.now())


class PharmacistProfile(BaseModel):
    """
    Extended profile for users with role=PHARMACIST. Stores the credentials
    required to legally review and approve prescriptions — license number
    and verification status are mandatory before a pharmacist account is
    allowed to action any PrescriptionReview.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="pharmacist_profile"
    )
    license_number = models.CharField(max_length=100, unique=True)
    license_authority = models.CharField(
        max_length=255, help_text="Issuing regulatory authority, e.g. Pharmacy Council"
    )
    license_document_url = models.URLField(blank=True)
    is_verified = models.BooleanField(
        default=False,
        help_text="Must be verified by Admin before pharmacist can review prescriptions",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="pharmacists_verified"
    )
    specialization = models.CharField(max_length=255, blank=True)
    years_of_experience = models.PositiveSmallIntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=["is_verified"])]

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.license_number}"


class Address(BaseModel):
    """Customer address book entry — supports multiple shipping/billing addresses per user."""

    class AddressType(models.TextChoices):
        SHIPPING = "SHIPPING", "Shipping"
        BILLING = "BILLING", "Billing"
        BOTH = "BOTH", "Both"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_type = models.CharField(
        max_length=10, choices=AddressType.choices, default=AddressType.BOTH
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=17)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, db_index=True)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Pakistan")
    is_default = models.BooleanField(default=False)
    delivery_instructions = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Addresses"
        indexes = [models.Index(fields=["user", "is_default"])]

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.country}"

    def save(self, *args, **kwargs):
        # Ensure only one default address per user
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(
                pk=self.pk
            ).update(is_default=False)
        super().save(*args, **kwargs)
