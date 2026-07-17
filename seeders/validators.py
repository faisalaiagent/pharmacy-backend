"""
seeders/validators.py

Validation utilities for the Pharmacy Seeder.
"""

from decimal import Decimal


class ValidationError(Exception):
    """Raised when generated seed data is invalid."""
    pass


class ProductValidator:

    REQUIRED_FIELDS = (
        "name",
        "generic_name",
        "category",
        "brand",
        "manufacturer",
        "price",
        "cost_price",
        "sku",
    )

    @classmethod
    def validate_required(cls, product):

        for field in cls.REQUIRED_FIELDS:

            if field not in product:
                raise ValidationError(
                    f"Missing required field: {field}"
                )

            value = product[field]

            if value is None:
                raise ValidationError(
                    f"{field} cannot be None"
                )

            if isinstance(value, str) and not value.strip():
                raise ValidationError(
                    f"{field} cannot be empty"
                )

    @staticmethod
    def validate_prices(product):

        price = Decimal(str(product["price"]))
        cost = Decimal(str(product["cost_price"]))

        discount = product.get("discount_price")

        if price <= 0:
            raise ValidationError(
                "Price must be greater than zero."
            )

        if cost <= 0:
            raise ValidationError(
                "Cost price must be greater than zero."
            )

        if cost > price:
            raise ValidationError(
                "Cost price cannot exceed retail price."
            )

        if discount is not None:

            discount = Decimal(str(discount))

            if discount > price:
                raise ValidationError(
                    "Discount cannot exceed price."
                )

            if discount <= 0:
                raise ValidationError(
                    "Discount must be positive."
                )

    @staticmethod
    def validate_stock(product):

        quantity = product.get(
            "stock_quantity",
            0,
        )

        if quantity < 0:
            raise ValidationError(
                "Negative stock not allowed."
            )

    @staticmethod
    def validate_strings(product):

        limits = {

            "name": 255,

            "generic_name": 255,

            "strength": 100,

            "dosage_form": 100,

            "batch_number": 100,

            "regulatory_approval_number": 100,

            "sku": 100,

        }

        for field, limit in limits.items():

            value = product.get(field)

            if value and len(str(value)) > limit:

                raise ValidationError(

                    f"{field} exceeds {limit} characters."

                )

    @staticmethod
    def validate_dates(product):

        expiry = product.get("expiry_date")

        if expiry is None:
            return

        from datetime import date

        if expiry <= date.today():

            raise ValidationError(

                "Expiry date must be in the future."

            )

    @classmethod
    def validate(cls, product):

        try:
            cls.validate_required(product)
            cls.validate_prices(product)
            cls.validate_stock(product)
            cls.validate_strings(product)
            cls.validate_dates(product)

        except ValidationError as e:

            print("\nValidation Failed")
            print(e)
            print("\nGenerated Keys:")
            print(sorted(product.keys()))

            raise

        return True


def validate_product(product):

    """
    Shortcut helper.

    Raises ValidationError on failure.
    """

    return ProductValidator.validate(product)