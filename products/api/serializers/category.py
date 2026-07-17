from rest_framework import serializers

from products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Category list/detail serializer.
    """

    product_count = serializers.SerializerMethodField()
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Category

        fields = (
            "id",
            "name",
            "slug",
            "description",
            "icon",
            "image",
            "parent",
            "parent_name",
            "is_featured",
            "display_order",
            "product_count",
        )

    def get_product_count(self, obj):
        return obj.products.count()

    def get_parent_name(self, obj):
        if obj.parent:
            return obj.parent.name
        return None