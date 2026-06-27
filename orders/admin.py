from django.contrib import admin

from .models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name_snapshot", "product_sku_snapshot", "unit_price", "line_total")


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ("status", "note", "changed_by", "created_at")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number", "user", "status", "payment_status",
        "total_amount", "requires_prescription_verification", "created_at"
    )
    list_filter = ("status", "payment_status", "requires_prescription_verification")
    search_fields = ("order_number", "user__email", "tracking_number")
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    readonly_fields = ("order_number", "subtotal", "total_amount")
