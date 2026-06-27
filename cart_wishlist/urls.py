from django.urls import path
from .views import (
    CartView, AddToCartView, UpdateCartItemView, RemoveCartItemView, ClearCartView,
    WishlistView, RemoveWishlistItemView,
)

app_name = "cart_wishlist"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="cart-add"),
    path("items/<uuid:item_id>/", UpdateCartItemView.as_view(), name="cart-item-update"),
    path("items/<uuid:item_id>/remove/", RemoveCartItemView.as_view(), name="cart-item-remove"),
    path("clear/", ClearCartView.as_view(), name="cart-clear"),

    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path("wishlist/<uuid:product_id>/remove/", RemoveWishlistItemView.as_view(), name="wishlist-remove"),
]
