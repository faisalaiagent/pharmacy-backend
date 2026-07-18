from rest_framework import serializers
from .models import Category, Brand, Manufacturer, Product, ProductImage, Inventory, Review


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "icon", "image",
                  "parent", "is_featured", "display_order", "children",
                  "meta_title", "meta_description")

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True).data


class CategoryFlatSerializer(serializers.ModelSerializer):
    """Lightweight version without recursive children — used in product listings."""
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "icon")


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name", "slug", "logo", "description")


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ("id", "name", "slug", "country", "logo", "website")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image_url", "alt_text", "is_primary", "display_order")


class InventorySerializer(serializers.ModelSerializer):
    quantity_available = serializers.ReadOnlyField()

    class Meta:
        model = Inventory
        fields = ("quantity_on_hand", "quantity_reserved", "quantity_available",
                  "warehouse_location", "reorder_point", "last_restocked_at")


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.CharField(source="user.avatar", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "user_name", "user_avatar", "rating", "title",
                  "comment", "is_verified_purchase", "helpful_count", "created_at")
        read_only_fields = ("id", "user_name", "user_avatar", "is_verified_purchase",
                            "helpful_count", "created_at")

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list/search pages — omits heavy text fields."""
    primary_image = serializers.SerializerMethodField()
    brand_name = serializers.CharField(source="brand.name", default=None, read_only=True)
    final_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    categories = CategoryFlatSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "sku", "generic_name", "strength", "package_size",
                  "product_type", "brand_name", "categories", "primary_image", "short_description",
                  "price", "discount_price", "final_price", "discount_percentage",
                  "stock_status", "requires_prescription",
                  "average_rating", "review_count", "is_featured", "is_best_seller")

    def get_primary_image(self, obj):
        img = obj.images.filter(is_primary=True).first() or obj.images.first()
        return img.image_url if img else None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for product detail page — includes all clinical content."""
    images = ProductImageSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    categories = CategoryFlatSerializer(many=True, read_only=True)
    inventory = InventorySerializer(read_only=True)
    final_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "sku", "product_type",
                  "generic_name", "strength", "dosage_form", "package_size",
                  "brand", "manufacturer", "categories", "images",
                  "short_description", "description", "ingredients",
                  "usage_instructions", "dosage_information", "side_effects",
                  "precautions", "contraindications", "storage_instructions",
                  "requires_prescription", "is_controlled_substance",
                  "regulatory_approval_number",
                  "price", "discount_price", "final_price", "discount_percentage",
                  "tax_rate", "stock_status", "stock_quantity",
                  "average_rating", "review_count",
                  "is_featured", "is_best_seller", "expiry_date",
                  "meta_title", "meta_description",
                  "inventory", "created_at")


class ProductWriteSerializer(serializers.ModelSerializer):
    """Admin create/update — accepts IDs for FK/M2M fields."""
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), source="categories", required=False
    )

    class Meta:
        model = Product
        exclude = ("average_rating", "review_count", "stock_quantity", "stock_status")

    def validate(self, attrs):
        discount = attrs.get("discount_price")
        price = attrs.get("price")
        if discount is not None and price is not None and discount > price:
            raise serializers.ValidationError({"discount_price": "Discount price cannot exceed regular price."})
        return attrs
