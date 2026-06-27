from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, ProfileView,
    ChangePasswordView, PasswordResetRequestView,
    AddressListCreateView, AddressDetailView, SetDefaultAddressView,
    UserListView, UserDetailAdminView, VerifyPharmacistView,
)

app_name = "users"

urlpatterns = [
    # Auth
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", ChangePasswordView.as_view(), name="change-password"),
    path("password/reset/", PasswordResetRequestView.as_view(), name="reset-password"),

    # Profile
    path("profile/", ProfileView.as_view(), name="profile"),

    # Addresses
    path("addresses/", AddressListCreateView.as_view(), name="address-list"),
    path("addresses/<uuid:pk>/", AddressDetailView.as_view(), name="address-detail"),
    path("addresses/<uuid:pk>/set-default/", SetDefaultAddressView.as_view(), name="address-set-default"),

    # Admin
    path("admin/users/", UserListView.as_view(), name="admin-user-list"),
    path("admin/users/<uuid:pk>/", UserDetailAdminView.as_view(), name="admin-user-detail"),
    path("admin/pharmacists/<uuid:pk>/verify/", VerifyPharmacistView.as_view(), name="verify-pharmacist"),
]
