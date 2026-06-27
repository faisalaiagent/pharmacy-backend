from django.urls import path
from .views import AdminDashboardView

app_name = "core"

urlpatterns = [
    path("", AdminDashboardView.as_view(), name="admin-dashboard"),
]
