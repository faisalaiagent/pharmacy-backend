"""
seeders/matcher.py

Production-grade matching engine for the Pharmacy Seeder.

Responsibilities
----------------
✓ Find Category
✓ Find Manufacturer
✓ Find Brand
✓ Keep relationships realistic
✓ Cache database lookups
"""

from __future__ import annotations

import random

from products.models import (
    Category,
    Manufacturer,
    Brand,
)


class Matcher:

    def __init__(self):

        self.categories = {
            c.name: c
            for c in Category.objects.filter(is_active=True)
        }

        self.manufacturers = list(
            Manufacturer.objects.filter(is_active=True)
        )

        self.brands = list(
            Brand.objects.filter(is_active=True)
            .select_related("manufacturer")
        )

    # ---------------------------------------------------------

    # CATEGORY

    # ---------------------------------------------------------

    def category(self, category_name):

        return self.categories.get(category_name)

    # ---------------------------------------------------------

    # MANUFACTURER

    # ---------------------------------------------------------

    def manufacturer(self):

        if not self.manufacturers:
            return None

        return random.choice(self.manufacturers)

    # ---------------------------------------------------------

    # BRAND

    # ---------------------------------------------------------

    def brand(self, manufacturer=None):

        if manufacturer is None:

            return random.choice(self.brands)

        brands = [

            b

            for b in self.brands

            if b.manufacturer_id == manufacturer.id

        ]

        if brands:

            return random.choice(brands)

        return random.choice(self.brands)

    # ---------------------------------------------------------

    # COMPLETE MATCH

    # ---------------------------------------------------------

    def match(self, medicine):

        """
        medicine example

        {
            "generic_name":"Paracetamol",
            "category":"Pain Relief",
            ...
        }
        """

        category = self.category(
            medicine["category"]
        )

        manufacturer = self.manufacturer()

        brand = self.brand(
            manufacturer
        )

        return {

            "category": category,

            "manufacturer": manufacturer,

            "brand": brand,

        }


_matcher = None


def get_matcher():

    global _matcher

    if _matcher is None:

        _matcher = Matcher()

    return _matcher


def match_product(medicine):

    return get_matcher().match(medicine)