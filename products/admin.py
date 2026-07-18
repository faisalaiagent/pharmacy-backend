from django.contrib import admin

from .models import Category, Brand, Manufacturer, Product, ProductImage, Inventory, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_featured", "is_active", "display_order")
    list_filter = ("is_featured", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "license_number", "is_active")
    search_fields = ("name", "license_number")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", "sku", "product_type", "price", "discount_price",
        "package_size ", "stock_status", "requires_prescription", "is_active", "is_featured"
    )
    list_filter = (
        "product_type", "stock_status", "requires_prescription",
        "is_controlled_substance", "is_featured", "is_best_seller", "is_active"
    )
    search_fields = ("name", "sku", "generic_name")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, InventoryInline]
    filter_horizontal = ("categories",)
    fieldsets = (
        ("Identity", {"fields": ("name", "slug", "sku", "product_type", "brand", "manufacturer", "categories")}),
        ("Pharma details", {"fields": ("generic_name", "strength", "dosage_form")}),
        ("Content", {"fields": (
            "short_description", "description", "ingredients", "usage_instructions",
            "dosage_information", "side_effects", "precautions", "contraindications",
            "storage_instructions"
        )}),
        ("Regulatory", {"fields": (
            "requires_prescription", "is_controlled_substance", "regulatory_approval_number"
        )}),
        ("Pricing", {"fields": ("price", "discount_price", "cost_price", "tax_rate")}),
        ("Stock", {"fields": ("stock_status", "stock_quantity", "low_stock_threshold")}),
        ("Flags", {"fields": ("is_featured", "is_best_seller", "is_active", "expiry_date", "batch_number")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "is_approved", "is_verified_purchase", "created_at")
    list_filter = ("rating", "is_approved", "is_verified_purchase")
    search_fields = ("product__name", "user__email")
