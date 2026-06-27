"""
Root URL configuration for the Pharmaceutical E-Commerce Platform.

Per-app API routes are namespaced under /api/v1/<app>/ and included from
each app's own urls.py (created in the next build stage, alongside the
serializers and views). This file wires the cross-cutting concerns that
don't belong to any single app: admin, JWT token endpoints, and API docs.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT token refresh/verify (obtain-token lives in users app — it's a
    # custom view there since login is by email, with role + extra claims)
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API documentation
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # App-level API routes (each app owns its own urls.py)
    path("api/v1/auth/", include("users.urls")),
    path("api/v1/products/", include("products.urls")),
    path("api/v1/orders/", include("orders.urls")),
    path("api/v1/prescriptions/", include("prescriptions.urls")),
    path("api/v1/cart/", include("cart_wishlist.urls")),
    path("api/v1/payments/", include("payments.urls")),
    path("api/v1/coupons/", include("coupons.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
    path("api/v1/content/", include("content.urls")),
    path("api/v1/ai/", include("ai_assistant.urls")),
    path("api/v1/admin/dashboard/", include("core.urls")),
]
