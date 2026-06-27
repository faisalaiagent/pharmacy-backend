from django.contrib import admin

from .models import Prescription, PrescriptionItem, PrescriptionReview


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 0


class PrescriptionReviewInline(admin.TabularInline):
    model = PrescriptionReview
    extra = 0
    readonly_fields = ("pharmacist", "decision", "comments", "rejection_reason", "created_at")
    can_delete = False


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "assigned_pharmacist", "doctor_name", "created_at")
    list_filter = ("status", "file_type")
    search_fields = ("user__email", "patient_name", "doctor_name")
    inlines = [PrescriptionItemInline, PrescriptionReviewInline]
    readonly_fields = ("file_url", "file_type", "file_size_bytes")


@admin.register(PrescriptionReview)
class PrescriptionReviewAdmin(admin.ModelAdmin):
    list_display = ("prescription", "pharmacist", "decision", "created_at")
    list_filter = ("decision",)
    search_fields = ("prescription__user__email", "pharmacist__email")
