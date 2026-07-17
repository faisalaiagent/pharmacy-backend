from rest_framework import serializers

from products.models import Inventory


class InventorySerializer(serializers.ModelSerializer):

    quantity_available = serializers.ReadOnlyField()

    class Meta:
        model = Inventory

        fields = (
            "quantity_on_hand",
            "quantity_reserved",
            "quantity_available",
            "warehouse_location",
            "reorder_point",
            "reorder_quantity",
            "last_restocked_at",
        )