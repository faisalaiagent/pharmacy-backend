from rest_framework import serializers

from products.models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage

        fields = (
            "id",
            "image_url",
            "alt_text",
            "is_primary",
            "display_order",
        )