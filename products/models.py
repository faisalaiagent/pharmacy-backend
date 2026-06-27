from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify

from core.models import BaseModel, SoftDeleteModel
from users.models import User


class Category(SoftDeleteModel):
    """
    Product category with self-referential parent for nested categories
    (e.g. Health Products > Vitamins > Multivitamins). Tree depth is
    intentionally unbounded at the model layer; the frontend nav enforces
    a sane display depth.
    """
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.URLField(blank=True)
    image = models.URLField(blank=True, help_text="Cloudinary URL")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True,
        related_name="children"
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    display_order = models.PositiveIntegerField(default=0)

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["display_order", "name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["parent", "is_active"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Manufacturer(SoftDeleteModel):
    """The actual pharmaceutical manufacturer — distinct from Brand, since
    one manufacturer may produce many brands and vice versa via licensing."""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=275, unique=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(
        max_length=100, blank=True,
        help_text="Drug manufacturing license / regulatory registration number"
    )
    logo = models.URLField(blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(SoftDeleteModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=275, unique=True, blank=True)
    logo = models.URLField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(SoftDeleteModel):
    """
    Core product model covering both prescription medicines and general
    health/OTC products. Pharma-specific fields (generic_name, dosage,
    side_effects, requires_prescription) are kept on the same model rather
    than a separate Medicine subclass — simpler joins, and the vast
    majority of fields are shared across product types anyway.
    """

    class ProductType(models.TextChoices):
        MEDICINE = "MEDICINE", "Medicine"
        HEALTH_PRODUCT = "HEALTH_PRODUCT", "Health Product"
        MEDICAL_DEVICE = "MEDICAL_DEVICE", "Medical Device"
        SUPPLEMENT = "SUPPLEMENT", "Supplement"

    class StockStatus(models.TextChoices):
        IN_STOCK = "IN_STOCK", "In Stock"
        LOW_STOCK = "LOW_STOCK", "Low Stock"
        OUT_OF_STOCK = "OUT_OF_STOCK", "Out of Stock"
        DISCONTINUED = "DISCONTINUED", "Discontinued"

    # Identity
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    product_type = models.CharField(
        max_length=20, choices=ProductType.choices, default=ProductType.MEDICINE,
        db_index=True
    )

    # Pharma-specific identity
    generic_name = models.CharField(
        max_length=255, blank=True, db_index=True,
        help_text="Active pharmaceutical ingredient / generic drug name"
    )
    strength = models.CharField(
        max_length=100, blank=True, help_text="e.g. 500mg, 10mg/5ml"
    )
    dosage_form = models.CharField(
        max_length=100, blank=True,
        help_text="e.g. Tablet, Syrup, Injection, Capsule, Cream"
    )

    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="products"
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="products"
    )
    categories = models.ManyToManyField(Category, related_name="products")

    # Content
    short_description = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    ingredients = models.TextField(
        blank=True, help_text="Full ingredient / composition list"
    )
    usage_instructions = models.TextField(blank=True)
    dosage_information = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    precautions = models.TextField(blank=True)
    contraindications = models.TextField(blank=True)
    storage_instructions = models.TextField(blank=True)

    # Regulatory / compliance
    requires_prescription = models.BooleanField(default=False, db_index=True)
    is_controlled_substance = models.BooleanField(default=False)
    regulatory_approval_number = models.CharField(max_length=150, blank=True)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Internal — not exposed to customers"
    )
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))

    # Stock (denormalized convenience fields synced from Inventory for fast querying)
    stock_status = models.CharField(
        max_length=20, choices=StockStatus.choices, default=StockStatus.IN_STOCK,
        db_index=True
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=10)

    # Ratings (denormalized aggregate, recalculated on Review save via signal)
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("5"))]
    )
    review_count = models.PositiveIntegerField(default=0)

    # Flags
    is_featured = models.BooleanField(default=False, db_index=True)
    is_best_seller = models.BooleanField(default=False, db_index=True)
    expiry_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=100, blank=True)

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["generic_name"]),
            models.Index(fields=["is_active", "stock_status"]),
            models.Index(fields=["is_featured", "is_active"]),
            models.Index(fields=["requires_prescription"]),
            models.Index(fields=["price"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(discount_price__lte=models.F("price")) | models.Q(discount_price__isnull=True),
                name="discount_price_lte_price",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:280] + "-" + str(self.sku)[:15]
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percentage(self):
        if self.discount_price and self.price:
            return round((1 - (self.discount_price / self.price)) * 100, 0)
        return 0


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(help_text="Cloudinary URL")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]
        indexes = [models.Index(fields=["product", "is_primary"])]

    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)
        super().save(*args, **kwargs)


class Inventory(BaseModel):
    """
    Source-of-truth stock ledger, separate from Product.stock_quantity
    (which is a denormalized read-optimized cache). Supports multi-warehouse
    in future without touching the Product table.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="inventory")
    quantity_on_hand = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(
        default=0, help_text="Reserved by unconfirmed/pending orders"
    )
    warehouse_location = models.CharField(max_length=255, blank=True)
    reorder_point = models.PositiveIntegerField(default=10)
    reorder_quantity = models.PositiveIntegerField(default=50)
    last_restocked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Inventory"

    @property
    def quantity_available(self):
        return self.quantity_on_hand - self.quantity_reserved

    def __str__(self):
        return f"Inventory: {self.product.name} ({self.quantity_available} available)"


class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(
        default=True, help_text="Admin can unpublish abusive/spam reviews"
    )
    helpful_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["product", "user"], name="one_review_per_user_per_product")
        ]
        indexes = [
            models.Index(fields=["product", "is_approved"]),
        ]

    def __str__(self):
        return f"{self.rating}★ review by {self.user} on {self.product}"
