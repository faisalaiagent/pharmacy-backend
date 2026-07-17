"""
Root URL configuration for the Pharmaceutical E-Commerce Platform.

Per-app API routes are namespaced under /api/v1/<app>/ and included from
each app's own urls.py.
"""

from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [

    # ==========================================================
    # Django Admin
    # ==========================================================

    path(
        "admin/",
        admin.site.urls,
    ),

    # ==========================================================
    # Authentication
    # ==========================================================

    path(
        "api/v1/auth/",
        include("users.urls"),
    ),

    path(
        "api/v1/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # ==========================================================
    # API Documentation
    # ==========================================================

    path(
        "api/v1/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),

    path(
        "api/v1/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema",
        ),
        name="redoc",
    ),

    # ==========================================================
    # Products
    # ==========================================================

    path(
        "api/v1/products/",
        include("products.urls"),
    ),

    # ==========================================================
    # Orders
    # ==========================================================

    path(
        "api/v1/orders/",
        include("orders.urls"),
    ),

    # ==========================================================
    # Prescriptions
    # ==========================================================

    path(
        "api/v1/prescriptions/",
        include("prescriptions.urls"),
    ),

    # ==========================================================
    # Cart / Wishlist
    # ==========================================================

    path(
        "api/v1/cart/",
        include("cart_wishlist.urls"),
    ),

    # ==========================================================
    # Payments
    # ==========================================================

    path(
        "api/v1/payments/",
        include("payments.urls"),
    ),

    # ==========================================================
    # Coupons
    # ==========================================================

    path(
        "api/v1/coupons/",
        include("coupons.urls"),
    ),

    # ==========================================================
    # Notifications
    # ==========================================================

    path(
        "api/v1/notifications/",
        include("notifications.urls"),
    ),

    # ==========================================================
    # Content / CMS
    # ==========================================================

    path(
        "api/v1/content/",
        include("content.urls"),
    ),

    # ==========================================================
    # AI Assistant
    # ==========================================================

    path(
        "api/v1/ai/",
        include("ai_assistant.urls"),
    ),

    # ==========================================================
    # Admin Dashboard APIs
    # ==========================================================

    path(
        "api/v1/admin/dashboard/",
        include("core.urls"),
    ),
]