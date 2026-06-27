from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from core.responses import success_response, error_response, created_response
from products.models import Product
from .models import Cart, CartItem, Wishlist
from .serializers import (
    CartSerializer, AddToCartSerializer, UpdateCartItemSerializer, WishlistSerializer
)


def get_or_create_cart(request):
    """Get or create a cart for the authenticated user."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return cart


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Cart"])
    def get(self, request):
        cart = get_or_create_cart(request)
        data = CartSerializer(cart).data
        return success_response(data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=AddToCartSerializer, tags=["Cart"])
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Invalid request.", serializer.errors)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return error_response("Product not found.", status_code=status.HTTP_404_NOT_FOUND)

        if product.stock_quantity < quantity:
            return error_response(
                f"Only {product.stock_quantity} unit(s) available in stock."
            )

        with transaction.atomic():
            cart = get_or_create_cart(request)
            item, created = CartItem.objects.get_or_create(
                cart=cart, product=product,
                defaults={"quantity": quantity}
            )
            if not created:
                new_qty = item.quantity + quantity
                if new_qty > product.stock_quantity:
                    return error_response(
                        f"Cannot add {quantity} more — only {product.stock_quantity - item.quantity} left."
                    )
                item.quantity = new_qty
                item.save(update_fields=["quantity"])

        cart_data = CartSerializer(cart).data
        msg = "Added to cart." if created else "Cart updated."
        return success_response(cart_data, msg)


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=UpdateCartItemSerializer, tags=["Cart"])
    def patch(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Invalid request.", serializer.errors)

        try:
            cart = Cart.objects.get(user=request.user)
            item = CartItem.objects.select_related("product").get(id=item_id, cart=cart)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return error_response("Cart item not found.", status_code=status.HTTP_404_NOT_FOUND)

        new_qty = serializer.validated_data["quantity"]
        if new_qty > item.product.stock_quantity:
            return error_response(f"Only {item.product.stock_quantity} unit(s) available.")

        item.quantity = new_qty
        item.save(update_fields=["quantity"])
        return success_response(CartSerializer(cart).data, "Cart updated.")


class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Cart"])
    def delete(self, request, item_id):
        try:
            cart = Cart.objects.get(user=request.user)
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
            return success_response(CartSerializer(cart).data, "Item removed from cart.")
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return error_response("Cart item not found.", status_code=status.HTTP_404_NOT_FOUND)


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Cart"])
    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            return success_response(message="Cart cleared.")
        except Cart.DoesNotExist:
            return success_response(message="Cart is already empty.")


# ── Wishlist ──────────────────────────────────────────────────────────────────

class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Wishlist"])
    def get(self, request):
        items = Wishlist.objects.filter(user=request.user).select_related(
            "product__brand"
        ).prefetch_related("product__images", "product__categories")
        data = WishlistSerializer(items, many=True, context={"request": request}).data
        return success_response(data)

    @extend_schema(tags=["Wishlist"])
    def post(self, request):
        """Add product to wishlist (idempotent — no error if already present)."""
        serializer = WishlistSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return error_response("Invalid request.", serializer.errors)

        product_id = serializer.validated_data["product_id"]
        product = Product.objects.get(id=product_id)
        item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        out = WishlistSerializer(item, context={"request": request}).data
        msg = "Added to wishlist." if created else "Already in wishlist."
        return created_response(out, msg) if created else success_response(out, msg)


class RemoveWishlistItemView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Wishlist"])
    def delete(self, request, product_id):
        deleted, _ = Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
        if deleted:
            return success_response(message="Removed from wishlist.")
        return error_response("Item not in wishlist.", status_code=status.HTTP_404_NOT_FOUND)
