from rest_framework import serializers

from products.models import Product

from .brand import BrandSerializer
from .manufacturer import ManufacturerSerializer
from .category import CategorySerializer
from .image import ProductImageSerializer


class ProductListSerializer(serializers.ModelSerializer):

    brand = BrandSerializer(read_only=True)

    manufacturer = ManufacturerSerializer(read_only=True)

    categories = CategorySerializer(many=True, read_only=True)

    primary_image = serializers.SerializerMethodField()

    final_price = serializers.ReadOnlyField()

    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product

        fields = (
            "id",
            "name",
            "slug",
            "sku",
            "generic_name",
            "strength",
            "dosage_form",
            "brand",
            "manufacturer",
            "categories",
            "price",
            "discount_price",
            "final_price",
            "discount_percentage",
            "stock_status",
            "average_rating",
            "review_count",
            "requires_prescription",
            "is_featured",
            "is_best_seller",
            "primary_image",
        )

    def get_primary_image(self, obj):

        image = obj.images.filter(
            is_primary=True
        ).first()

        if image:
            return ProductImageSerializer(image).data

        return None