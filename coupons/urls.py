from django.urls import path
from .views import ValidateCouponView, AdminCouponListCreateView

app_name = "coupons"

urlpatterns = [
    path("validate/", ValidateCouponView.as_view(), name="validate"),
    path("admin/", AdminCouponListCreateView.as_view(), name="admin-list"),
]
