from rest_framework import serializers

from products.models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    """
    Manufacturer serializer.
    """

    brand_count = serializers.SerializerMethodField()

    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Manufacturer

        fields = (
            "id",
            "name",
            "slug",
            "country",
            "license_number",
            "logo",
            "website",
            "description",
            "brand_count",
            "product_count",
        )

    def get_brand_count(self, obj):
        return obj.brands.count()

    def get_product_count(self, obj):
        return obj.products.count()