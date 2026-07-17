import random

from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from products.models import (
    Product,
    Inventory,
)
class InventorySeeder:

    def __init__(self):

        self.products = Product.objects.all()

        self.created = 0
        self.updated = 0
        self.skipped = 0

        self.errors = []

    def get_products(self):

        return self.products    
    
    def inventory_exists(
        self,
        product,
    ):

        return Inventory.objects.filter(
            product=product
        ).exists()
    
    def build_quantity(self):

        return random.randint(
            15,
            500,
        )
    
    def build_reserved(
        self,
        quantity,
    ):

        return random.randint(
            0,
            min(10, quantity),
        )
    
    WAREHOUSES = [

        "Karachi Warehouse",

        "Lahore Warehouse",

        "Islamabad Warehouse",

    ]

    def build_warehouse(self):

        return random.choice(
            self.WAREHOUSES
        )
    
    def build_reorder_point(self):

        return random.choice(

            [

                10,

                15,

                20,

                25,

            ]

        )
    
    def build_reorder_quantity(self):

        return random.choice(

            [

                50,

                100,

                150,

                200,

            ]

        )
    
    def build_last_restock(self):

        return (

            timezone.now()

            -

            timedelta(

                days=random.randint(
                    1,
                    120,
                )

            )

        )
    
    def build_defaults(
        self,
    ):

        quantity = self.build_quantity()

        return {

            "quantity_on_hand": quantity,

            "quantity_reserved": self.build_reserved(
                quantity,
            ),

            "warehouse_location": self.build_warehouse(),

            "reorder_point": self.build_reorder_point(),

            "reorder_quantity": self.build_reorder_quantity(),

            "last_restocked_at": self.build_last_restock(),

        }
    
    def validate_product(
        self,
        product,
    ):

        missing = []

        if product is None:
            missing.append("Product")

        return {

            "valid": len(missing) == 0,

            "missing": missing,

        }
    
    @transaction.atomic
    def seed_inventory(self, profile):

        result = self.validate_profile(profile)

        if not result["valid"]:

            self.errors.append(
                f"Product not found: {profile['brand_name']}"
            )

            return None

        product = result["product"]

        inventory, created = Inventory.objects.update_or_create(

            product=product,

            defaults=self.build_defaults(profile),
        )

        if created:
            self.created += 1
        else:
            self.updated += 1

        return inventory
    
    def seed(self):

        total = len(self.profiles)

        for index, profile in enumerate(self.profiles, start=1):

            print(
                f"{index}/{total} -> "
                f"{profile['brand_name']}"
            )

            self.seed_inventory(profile)

        print("\nFinished!")

        return self.summary()


    run = seed

    def summary(self):

        return {

            "created": self.created,

            "updated": self.updated,

            "skipped": self.skipped,

            "errors": len(self.errors),
        }
    
    def print_summary(self):

        print()

        print("=" * 60)

        print("Inventory Seeder")

        print("=" * 60)

        print(f"Created : {self.created}")
        print(f"Updated : {self.updated}")
        print(f"Skipped : {self.skipped}")
        print(f"Errors  : {len(self.errors)}")

        if self.errors:

            print()

            for error in self.errors:
                print(error)

        print("=" * 60)

        