"""
Production Pricing Engine
-------------------------

Generates realistic Pakistani pharmacy pricing.

Calculates:

- Cost Price
- Retail Price
- Discount Price
- Tax
- Profit Margin
- Savings
"""

from __future__ import annotations

import random
from decimal import Decimal, ROUND_HALF_UP


class PricingEngine:

    """
    Enterprise pricing engine.
    """

    CATEGORY_PRICE_RANGES = {

        "Pain Relief": (80, 450),

        "Antibiotics": (250, 2200),

        "Diabetes": (350, 3200),

        "Heart Care": (300, 4500),

        "Respiratory": (250, 3500),

        "Eye Care": (180, 1800),

        "ENT": (180, 1500),

        "Skin Care": (120, 2200),

        "Gastrointestinal": (180, 2500),

        "Women's Health": (200, 3500),

        "Men's Health": (300, 5000),

        "Pediatrics": (120, 1800),

        "Neurology": (600, 6500),

        "Oncology": (2500, 75000),

        "Oncology Supportive": (800, 8500),

        "Urology": (350, 4500),

        "Vitamin C": (150, 700),

        "Vitamin D": (180, 1200),

        "Multivitamins": (250, 2200),

        "Calcium": (220, 1800),

        "Iron": (180, 1200),

        "Zinc": (150, 900),

        "Omega 3": (450, 2800),

        "Protein": (1800, 12000),

        "Hair Care": (250, 2200),

        "Face Wash": (250, 1800),

        "Soap": (120, 450),

        "Shampoo": (250, 2800),

        "Conditioner": (250, 2200),

        "Toothpaste": (180, 850),

        "Toothbrush": (120, 650),

        "Deodorants": (250, 2200),

        "Baby Food": (650, 4500),

        "Baby Lotion": (250, 1800),

        "Baby Powder": (180, 1200),

        "Baby Shampoo": (280, 1800),

        "Diapers": (450, 4500),

        "BP Monitor": (2500, 12000),

        "Glucometer": (1800, 8500),

        "Thermometer": (450, 2500),

        "Nebulizer": (3500, 12000),

        "Wheelchair": (12000, 65000),

        "Pulse Oximeter": (1800, 6500),

        "First Aid": (350, 4500),

        "Condoms": (150, 1200),

        "Lubricants": (350, 1800),

        "Pregnancy Tests": (180, 1200),
    }

    DEFAULT_RANGE = (250, 1500)

    TAX_RATE = Decimal("18.00")

    @staticmethod
    def money(value):

        return Decimal(value).quantize(

            Decimal("0.01"),

            rounding=ROUND_HALF_UP,

        )

    @classmethod
    def category_range(

        cls,

        category_name,

    ):

        return cls.CATEGORY_PRICE_RANGES.get(

            category_name,

            cls.DEFAULT_RANGE,

        )

    @classmethod
    def retail_price(

        cls,

        category_name,

    ):

        low, high = cls.category_range(

            category_name

        )

        return cls.money(

            random.uniform(low, high)

        )

    @classmethod
    def cost_price(

        cls,

        retail,

    ):

        ratio = random.uniform(

            0.55,

            0.80,

        )

        return cls.money(

            retail * Decimal(str(ratio))

        )

    @classmethod
    def discount_price(

        cls,

        retail,

    ):

        if random.random() < 0.35:

            discount = random.uniform(

                5,

                20,

            )

            value = retail * Decimal(

                str(

                    1 - discount / 100

                )

            )

            return cls.money(value)

        return None

    @classmethod
    def margin(

        cls,

        retail,

        cost,

    ):

        return cls.money(

            retail - cost

        )

    @classmethod
    def savings(

        cls,

        retail,

        discount,

    ):

        if discount is None:

            return Decimal("0.00")

        return cls.money(

            retail - discount

        )

    @classmethod
    def tax(

        cls,

        retail,

    ):

        return cls.money(

            retail *

            cls.TAX_RATE /

            Decimal("100")

        )

    @classmethod
    def generate(

        cls,

        category_name,

    ):

        retail = cls.retail_price(

            category_name

        )

        cost = cls.cost_price(

            retail

        )

        discount = cls.discount_price(

            retail

        )

        return {

            "price": retail,

            "cost_price": cost,

            "discount_price": discount,

            "tax_rate": cls.TAX_RATE,

            "profit": cls.margin(

                retail,

                cost,

            ),

            "tax_amount": cls.tax(

                retail

            ),

            "savings": cls.savings(

                retail,

                discount,

            ),

        }


def generate_pricing(

    category_name,

):

    return PricingEngine.generate(

        category_name

    )