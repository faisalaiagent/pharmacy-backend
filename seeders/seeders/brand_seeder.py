from django.db import transaction

from products.models import (
    Brand,
    Manufacturer,
)

from seeders.repositories.brand_repository import (
    BrandRepository,
)


class BrandSeeder:
    """
    Imports brands.json into the Brand model.
    """

    def __init__(self):
        self.repo = BrandRepository()

        self.created = 0
        self.updated = 0
        self.skipped = 0
        self.errors = []

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def get_manufacturer(self, name):

        if not name:
            return None

        return Manufacturer.objects.filter(
            name=name
        ).first()

    def brand_exists(self, name):

        return Brand.objects.filter(
            name=name
        ).exists()

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_brand(self, profile):

        manufacturer = self.get_manufacturer(
            profile["manufacturer"]
        )

        return {
            "valid": manufacturer is not None,
            "manufacturer": manufacturer,
        }

    # ---------------------------------------------------------
    # Upsert
    # ---------------------------------------------------------

    @transaction.atomic
    def seed_brand(self, profile):

        result = self.validate_brand(profile)

        if not result["valid"]:

            self.errors.append(
                f"Manufacturer not found: "
                f'{profile["manufacturer"]}'
            )

            return None

        manufacturer = result["manufacturer"]

        brand, created = Brand.objects.update_or_create(

            name=profile["name"],

            defaults={
                "manufacturer": manufacturer,
                "description": "",
                "logo": "",
            },
        )

        if created:
            self.created += 1
        else:
            self.updated += 1

        return brand

    # ---------------------------------------------------------
    # Main
    # ---------------------------------------------------------

    def seed(self):

        total = self.repo.count()

        for index, profile in enumerate(self.repo.brands, start=1):

            print(f"{index}/{total} -> {profile['name']}")

            self.seed_brand(profile)

        print("\nFinished!")

        return self.summary()

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def summary(self):

        return {
            "created": self.created,
            "updated": self.updated,
            "skipped": self.skipped,
            "errors": len(self.errors),
        }

    def print_summary(self):

        print()

        print("=" * 50)

        print("Brand Seeder")

        print("=" * 50)

        print(f"Created : {self.created}")
        print(f"Updated : {self.updated}")
        print(f"Skipped : {self.skipped}")
        print(f"Errors  : {len(self.errors)}")

        if self.errors:

            print()

            for error in self.errors:
                print(error)

        print("=" * 50)