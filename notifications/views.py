from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from core.responses import success_response
from .models import Notification
from rest_framework import serializers as drf_serializers


class NotificationSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "notification_type", "channel", "title", "message",
                  "link_url", "is_read", "created_at")


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Notifications"])
    def get(self, request):
        qs = Notification.objects.filter(user=request.user).order_by("-created_at")
        unread_count = qs.filter(is_read=False).count()
        notifications = qs[:50]
        return success_response({
            "unread_count": unread_count,
            "notifications": NotificationSerializer(notifications, many=True).data,
        })


class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Notifications"])
    def post(self, request, pk):
        Notification.objects.filter(pk=pk, user=request.user).update(is_read=True)
        return success_response(message="Marked as read.")


class MarkAllReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Notifications"])
    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return success_response(message="All notifications marked as read.")
