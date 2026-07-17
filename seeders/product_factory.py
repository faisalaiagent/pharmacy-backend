"""
seeders/product_factory.py

Builds a complete product dictionary ready for insertion into
the Django Product model.

Responsibilities

✓ Match category
✓ Match manufacturer
✓ Match brand
✓ Generate pricing
✓ Generate SKU
✓ Generate batch number
✓ Generate regulatory information
✓ Validate final product
"""

from random import randint, random
from datetime import date, timedelta

from seeders.matcher import match_product
from seeders.pricing_engine import generate_pricing
from seeders.sku_generator import generate_sku
from seeders.batch_generator import generate_batch
from seeders.regulatory import generate_regulatory
from seeders.validators import validate_product


class ProductFactory:

    def __init__(self):
        pass

    def expiry_date(self):

        return date.today() + timedelta(
            days=randint(365, 365 * 3)
        )

    def stock_quantity(self):

        return randint(25, 500)

    def featured(self):

        return random() < 0.08

    def bestseller(self):

        return random() < 0.12

    def requires_prescription(self, medicine):

        category = medicine["category"]

        otc = {

            "Pain Relief",

            "Vitamin C",

            "Vitamin D",

            "Multivitamins",

            "Calcium",

            "Iron",

            "Zinc",

            "Omega 3",

            "Protein",

            "Soap",

            "Shampoo",

            "Hair Care",

            "Toothpaste",

            "Toothbrush",

            "Face Wash",

            "Baby Lotion",

            "Baby Powder",

            "Baby Shampoo",

            "Condoms",

            "Lubricants",

            "Pregnancy Tests",

        }

        return category not in otc

    def product_type(self, medicine):

        category = medicine["category"]

        devices = {

            "BP Monitor",

            "Nebulizer",

            "Thermometer",

            "Pulse Oximeter",

            "Wheelchair",

            "Glucometer",

        }

        personal = {

            "Soap",

            "Hair Care",

            "Face Wash",

            "Conditioner",

            "Shampoo",

            "Toothpaste",

            "Toothbrush",

            "Deodorants",

        }

        supplements = {

            "Vitamin C",

            "Vitamin D",

            "Multivitamins",

            "Calcium",

            "Iron",

            "Zinc",

            "Omega 3",

            "Protein",

        }

        if category in devices:
            return "device"

        if category in personal:
            return "personal_care"

        if category in supplements:
            return "supplement"

        return "medicine"

    def build(self, medicine):

        matched = match_product(medicine)

        pricing = generate_pricing(
            medicine["category"]
        )

        regulatory = generate_regulatory()

        sku = generate_sku(
            manufacturer=matched["manufacturer"].name,
            generic_name=medicine["generic_name"],
            dosage_form=medicine["dosage_form"],
            strength=medicine["strength"],
        )

        batch = generate_batch()

        product = {

            "name": f'{matched["brand"].name} {medicine["strength"]}',

            "generic_name": medicine["generic_name"],

            "strength": medicine["strength"],

            "dosage_form": medicine["dosage_form"],

            "category": matched["category"],

            "manufacturer": matched["manufacturer"],

            "brand": matched["brand"],

            "sku": sku,

            "batch_number": batch,

            "expiry_date": self.expiry_date(),

            "stock_quantity": self.stock_quantity(),

            "requires_prescription":
                self.requires_prescription(medicine),

            "product_type":
                self.product_type(medicine),

            "is_featured":
                self.featured(),

            "is_best_seller":
                self.bestseller(),

            "price":
                pricing["price"],

            "discount_price":
                pricing["discount_price"],

            "cost_price":
                pricing["cost_price"],

            "tax_rate":
                pricing["tax_rate"],

            "regulatory_approval_number":
                regulatory["regulatory_approval_number"],

            "description":
                medicine.get("description", ""),

            "ingredients":
                medicine.get("ingredients", ""),

            "usage_instructions":
                medicine.get("usage", ""),

            "dosage_information":
                medicine.get("dosage", ""),

            "side_effects":
                medicine.get("side_effects", ""),

            "precautions":
                medicine.get("precautions", ""),

            "contraindications":
                medicine.get("contraindications", ""),

            "storage_instructions":
                medicine.get("storage", ""),

            "meta_title":
                f'{matched["brand"].name} {medicine["strength"]}',

            "meta_description":
                medicine.get("description", "")[:160],

        }

        validate_product(product)

        return product


_factory = ProductFactory()


def build_product(medicine):

    return _factory.build(medicine)