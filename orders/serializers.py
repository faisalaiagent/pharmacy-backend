from rest_framework import serializers
from users.serializers import AddressSerializer
from .models import Order, OrderItem, OrderStatusHistory


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_name_snapshot", "product_sku_snapshot",
                  "unit_price", "quantity", "line_total", "required_prescription")


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.CharField(source="changed_by.get_full_name", default=None)

    class Meta:
        model = OrderStatusHistory
        fields = ("status", "note", "changed_by_name", "created_at")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    shipping_address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "order_number", "status", "payment_status",
                  "items", "status_history",
                  "shipping_address", "shipping_address_snapshot",
                  "subtotal", "discount_amount", "tax_amount",
                  "shipping_amount", "total_amount",
                  "coupon_code", "requires_prescription_verification",
                  "tracking_number", "courier_name", "estimated_delivery_date",
                  "customer_notes", "created_at")
        read_only_fields = ("id", "order_number", "status", "payment_status",
                            "subtotal", "total_amount", "created_at")


class PlaceOrderSerializer(serializers.Serializer):
    shipping_address_id = serializers.UUIDField()
    billing_address_id = serializers.UUIDField(required=False)
    payment_method = serializers.ChoiceField(choices=["STRIPE", "PAYPAL", "COD"])
    coupon_code = serializers.CharField(required=False, allow_blank=True)
    prescription_id = serializers.UUIDField(required=False)
    customer_notes = serializers.CharField(required=False, allow_blank=True)


class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)
    note = serializers.CharField(required=False, allow_blank=True)
    tracking_number = serializers.CharField(required=False, allow_blank=True)
    courier_name = serializers.CharField(required=False, allow_blank=True)
