from rest_framework import serializers

from products.models import Product

from .brand import BrandSerializer
from .manufacturer import ManufacturerSerializer
from .category import CategorySerializer
from .image import ProductImageSerializer
from .inventory import InventorySerializer
from .review import ReviewSerializer


class ProductDetailSerializer(serializers.ModelSerializer):

    brand = BrandSerializer(read_only=True)

    manufacturer = ManufacturerSerializer(read_only=True)

    categories = CategorySerializer(
        many=True,
        read_only=True,
    )

    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    inventory = InventorySerializer(
        read_only=True,
    )

    reviews = ReviewSerializer(
        many=True,
        read_only=True,
    )

    final_price = serializers.ReadOnlyField()

    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product

        fields = "__all__"