from django.contrib import admin

from .models import Coupon, CouponUsage


class CouponUsageInline(admin.TabularInline):
    model = CouponUsage
    extra = 0
    readonly_fields = ("user", "order", "created_at")
    can_delete = False


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code", "discount_type", "discount_value", "times_used",
        "usage_limit", "is_active", "valid_from", "valid_until"
    )
    list_filter = ("discount_type", "is_active")
    search_fields = ("code",)
    filter_horizontal = ("applicable_categories",)
    inlines = [CouponUsageInline]
