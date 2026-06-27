from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("notification_type", "user", "is_admin_alert", "channel", "is_read", "is_sent", "created_at")
    list_filter = ("notification_type", "channel", "is_read", "is_sent", "is_admin_alert")
    search_fields = ("user__email", "title")
