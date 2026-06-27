from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "method", "status", "amount", "currency", "paid_at", "created_at")
    list_filter = ("method", "status", "currency")
    search_fields = ("order__order_number", "gateway_transaction_id", "gateway_payment_intent_id")
    readonly_fields = ("gateway_response",)
