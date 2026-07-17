from urllib.parse import quote

from django.db import transaction

from products.models import (
    ProductImage,
)

from seeders.repositories.product_repository import (
    ProductRepository,
)


class ProductImageSeeder:
    """
    Creates one primary image for every product.
    """

    IMAGE_BASE = "https://dummyimage.com/"

    DEFAULT_SIZE = "900x900"
    DEFAULT_BG = "ffffff"
    DEFAULT_TEXT = "333333"

    def __init__(self):

        self.repo = ProductRepository()

        self.products = self.repo.products

        self.created = 0
        self.updated = 0
        self.skipped = 0
        self.errors = []

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def count(self):
        return len(self.products)

    def build_image_url(self, product):

        text = quote(product.name)

        return (
            f"{self.IMAGE_BASE}"
            f"{self.DEFAULT_SIZE}/"
            f"{self.DEFAULT_BG}/"
            f"{self.DEFAULT_TEXT}"
            f"?text={text}"
        )

    def build_alt_text(self, product):

        parts = [
            product.name,
            product.strength,
            product.dosage_form,
        ]

        return " ".join(
            p for p in parts if p
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_product(self, product):

        if product is None:
            return False

        if not product.name:
            return False

        return True

    def image_exists(
        self,
        product,
        image_url,
    ):

        return ProductImage.objects.filter(
            product=product,
            image_url=image_url,
        ).exists()

    # ---------------------------------------------------------
    # Defaults
    # ---------------------------------------------------------

    def build_defaults(self, product):

        return {
            "alt_text": self.build_alt_text(product),
            "is_primary": True,
            "display_order": 1,
        }

    # ---------------------------------------------------------
    # Upsert
    # ---------------------------------------------------------

    @transaction.atomic
    def seed_image(self, product):

        if not self.validate_product(product):

            self.skipped += 1

            self.errors.append(
                f"Invalid product: {product}"
            )

            return None

        image_url = self.build_image_url(product)

        image, created = ProductImage.objects.update_or_create(

            product=product,

            image_url=image_url,

            defaults=self.build_defaults(product),

        )

        if created:
            self.created += 1
        else:
            self.updated += 1

        return image

    # ---------------------------------------------------------
    # Main
    # ---------------------------------------------------------

    def seed(self):

        total = self.count()

        for index, product in enumerate(self.products, start=1):

            print(
                f"{index}/{total} -> {product.name}"
            )

            self.seed_image(product)

        print("\nFinished!")

        return self.summary()

    run = seed

    # ---------------------------------------------------------
    # Reporting
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
        print("Product Image Seeder")
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