from rest_framework import serializers

from products.models import Brand

from .manufacturer import ManufacturerSerializer


class BrandSerializer(serializers.ModelSerializer):
    """
    Brand serializer.
    """

    manufacturer = ManufacturerSerializer(read_only=True)

    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Brand

        fields = (
            "id",
            "name",
            "slug",
            "logo",
            "description",
            "manufacturer",
            "product_count",
        )

    def get_product_count(self, obj):
        return obj.products.count()