from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, PharmacistProfile, Address


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "role", "is_active", "email_verified", "created_at")
    list_filter = ("role", "is_active", "email_verified", "phone_verified")
    search_fields = ("email", "username", "phone_number")
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number", "date_of_birth", "avatar")}),
        ("Role & permissions", {
            "fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Verification", {"fields": ("email_verified", "phone_verified")}),
        ("Security", {"fields": ("failed_login_attempts", "locked_until", "last_login_ip")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(PharmacistProfile)
class PharmacistProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "license_number", "is_verified", "years_of_experience")
    list_filter = ("is_verified",)
    search_fields = ("user__email", "license_number")
    actions = ["verify_pharmacists"]

    @admin.action(description="Mark selected pharmacists as verified")
    def verify_pharmacists(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_verified=True, verified_at=timezone.now(), verified_by=request.user)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "city", "country", "is_default")
    list_filter = ("country", "is_default")
    search_fields = ("user__email", "full_name", "city")
