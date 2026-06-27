from django.urls import path
from .views import NotificationListView, MarkNotificationReadView, MarkAllReadView

app_name = "notifications"

urlpatterns = [
    path("", NotificationListView.as_view(), name="list"),
    path("<uuid:pk>/read/", MarkNotificationReadView.as_view(), name="mark-read"),
    path("read-all/", MarkAllReadView.as_view(), name="mark-all-read"),
]
