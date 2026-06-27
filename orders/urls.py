from django.urls import path
from .views import (
    PlaceOrderView, OrderListView, OrderDetailView, CancelOrderView,
    AdminOrderListView, AdminUpdateOrderStatusView,
)

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("place/", PlaceOrderView.as_view(), name="place-order"),
    path("<uuid:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("<str:order_number>/cancel/", CancelOrderView.as_view(), name="cancel-order"),

    # Admin
    path("admin/", AdminOrderListView.as_view(), name="admin-order-list"),
    path("admin/<str:order_number>/status/", AdminUpdateOrderStatusView.as_view(), name="admin-order-status"),
]
