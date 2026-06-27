from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from core.models import BaseModel
from users.models import User
from products.models import Product


class Cart(BaseModel):
    """
    One active cart per user. Guest carts are supported via session_key so
    anonymous browsing/cart-building works pre-login, then merges into the
    user's cart on authentication (handled in the API layer, not here).
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cart", null=True, blank=True
    )
    session_key = models.CharField(
        max_length=64, blank=True, db_index=True,
        help_text="For guest/anonymous carts prior to login"
    )

    class Meta:
        indexes = [models.Index(fields=["session_key"])]

    def __str__(self):
        return f"Cart - {self.user or self.session_key}"

    @property
    def subtotal(self):
        return sum((item.line_total for item in self.items.all()), Decimal("0.00"))

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    # Snapshot price at add-to-cart time isn't stored here — cart is transient
    # and always reflects live Product pricing until checkout, where Order
    # line items DO snapshot price (see orders.OrderItem).

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["cart", "product"], name="unique_product_per_cart")
        ]

    @property
    def line_total(self):
        return self.product.final_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_wishlist_entry")
        ]
        indexes = [models.Index(fields=["user"])]

    def __str__(self):
        return f"{self.user} ♥ {self.product.name}"
