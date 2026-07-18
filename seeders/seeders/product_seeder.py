from __future__ import annotations

from decimal import Decimal
import random


from django.db import transaction
from django.utils.text import slugify

from products.models import (
    Product,
    Brand,
    Category,
    Manufacturer,
)

from ..repositories.brand_profile_repository import (
    BrandProfileRepository,
)

from ..repositories.brand_repository import (
    BrandRepository,
)

from ..repositories.manufacturer_repository import (
    ManufacturerRepository,
)

from ..repositories.medicine_profile_repository import (
    MedicineProfileRepository,
)

class ProductSeeder:
    """
    Seeds Product objects from brand profiles.
    """

    def __init__(self):

        self.brand_profiles = BrandProfileRepository()

        self.brand_repo = BrandRepository()

        self.manufacturer_repo = ManufacturerRepository()

        self.medicine_repo = MedicineProfileRepository()

        self.created = 0

        self.updated = 0

        self.skipped = 0

        self.errors = []

        self.verbose = True

    def log(
        self,
        message,
    ):

        if self.verbose:
            print(message)  

    def reset(self):

        self.created = 0

        self.updated = 0

        self.skipped = 0

        self.errors = []

    def summary(self):

        return {

            "created": self.created,

            "updated": self.updated,

            "skipped": self.skipped,

            "errors": len(self.errors),

        }              
    
    @property
    def profiles(self):

        return self.brand_profiles.profiles

    def count(self):

        return len(self.profiles)
    
    def preview(
        self,
        limit=5,
    ):

        for profile in self.profiles[:limit]:

            print(profile)

    def get_brand(
        self,
        brand_name,
    ):
        """
        Return Brand model instance.
        """

        try:

            return Brand.objects.get(
                name=brand_name,
            )

        except Brand.DoesNotExist:

            return None
        
    def get_manufacturer(
        self,
        manufacturer_name,
    ):
        """
        Return Manufacturer model instance.
        """

        try:

            return Manufacturer.objects.get(
                name=manufacturer_name,
            )

        except Manufacturer.DoesNotExist:

            return None

    def get_category(
         self,
        category_name,
    ):
        """
        Return Category model instance.
        """

        try:

            return Category.objects.get(
                name=category_name,
            )

        except Category.DoesNotExist:

            return None

    def product_exists(
        self,
        sku,
    ):
        """
        Returns True if product already exists.
        """

        return Product.objects.filter(
            sku=sku,
        ).exists()

    def get_product(
        self,
        sku,
    ):
        """
        Return Product instance by SKU.
        """

        try:

            return Product.objects.get(
                sku=sku,
            )

        except Product.DoesNotExist:

            return None

    def validate_profile(
        self,
        profile,
    ):
        """
        Ensure related database records exist.
        """

        brand = self.get_brand(
            profile["brand_name"]
        )

        manufacturer = self.get_manufacturer(
            profile["manufacturer"]
        )

        category = self.get_category(
            profile["category"]
        )

        missing = []

        if brand is None:
            missing.append("Brand")

        if manufacturer is None:
            missing.append("Manufacturer")

        if category is None:
            missing.append("Category")

        return {

            "valid": len(missing) == 0,

            "brand": brand,

            "manufacturer": manufacturer,

            "category": category,

            "missing": missing,

        }               

    def validate_profiles(
        self,
    ):
        """
        Validate every brand profile.
        """

        report = []

        for profile in self.profiles:

            result = self.validate_profile(
                profile
            )

            if not result["valid"]:

                report.append(
                    {
                        "brand": profile["brand_name"],
                        "missing": result["missing"],
                    }
                )

        return report
    
    def build_defaults(
        self,
        profile,
        brand,
        manufacturer,
    ):
        """
        Build Product defaults for update_or_create().
        """

        price = Decimal(str(profile["price"]))

        # 5–15% discount (roughly 40% of products)
        if random.random() < 0.40:

            percent = random.randint(5, 15)

            discount_price = (
                price * Decimal(100 - percent) / Decimal(100)
            ).quantize(Decimal("0.01"))

        else:
            discount_price = None

        # Internal purchase cost (~65% of selling price)
        cost_price = (
            price * Decimal("0.65")
        ).quantize(Decimal("0.01"))

        # Random stock

        stock_quantity = random.randint(
            10,
            250,
        )

        # Stock status

        if stock_quantity == 0:

            stock_status = (
                Product.StockStatus.OUT_OF_STOCK
            )

        elif stock_quantity <= 10:

            stock_status = (
                Product.StockStatus.LOW_STOCK
            )

        else:

            stock_status = (
                Product.StockStatus.IN_STOCK
            )

        brand_name = profile["brand_name"]

        generic = profile["generic_name"]

        return {

            # --------------------------------------------------
            # Identity
            # --------------------------------------------------

            "name": brand_name,

            "product_type":
                Product.ProductType.MEDICINE,

            "generic_name": generic,

            "strength":
                profile["strength"],

            "dosage_form":
                profile["dosage_form"],

            "package_size":
                profile.get("package_size", ""),    

            "brand": brand,

            "manufacturer": manufacturer,

            # --------------------------------------------------
            # Content
            # --------------------------------------------------

            "short_description":
                f"{generic} {profile['strength']} "
                f"{profile['dosage_form']}",

            "description":
                (
                    f"{brand_name} is a "
                    f"{profile['dosage_form'].lower()} "
                    f"containing {generic} "
                    f"{profile['strength']}."
                ),

            "ingredients":
                generic,

            "usage_instructions":
                "Use exactly as directed by your physician.",

            "dosage_information":
                (
                    f"{profile['strength']} "
                    f"{profile['dosage_form']}"
                ),

            "side_effects":
                "\n".join(
                    profile["side_effects"]
                ),

            "precautions":
                (
                    "Keep out of reach of children."
                ),

            "contraindications":
                "\n".join(
                    profile["contraindications"]
                ),

            "storage_instructions":
                "\n".join(
                    profile["storage"]
                ),

            # --------------------------------------------------
            # Regulatory
            # --------------------------------------------------

            "requires_prescription":
                profile["prescription_required"],

            "is_controlled_substance":
                False,

            "regulatory_approval_number":
                "",

            # --------------------------------------------------
            # Pricing
            # --------------------------------------------------

            "price":
                price,

            "discount_price":
                discount_price,

            "cost_price":
                cost_price,

            "tax_rate":
                Decimal("0.00"),

            # --------------------------------------------------
            # Stock
            # --------------------------------------------------

            "stock_status":
                stock_status,

            "stock_quantity":
                stock_quantity,

            "low_stock_threshold":
                10,

            # --------------------------------------------------
            # Ratings
            # --------------------------------------------------

            "average_rating":
                Decimal("0.00"),

            "review_count":
                0,

            # --------------------------------------------------
            # Flags
            # --------------------------------------------------

            "is_featured":
                random.random() < 0.10,

            "is_best_seller":
                random.random() < 0.05,

            "batch_number":
                f"BATCH-{random.randint(100000,999999)}",

            # --------------------------------------------------
            # SEO
            # --------------------------------------------------

            "meta_title":
                (
                    f"{brand_name} "
                    f"{profile['strength']} | "
                    f"{generic}"
                ),

            "meta_description":
                (
                    f"Buy {brand_name} "
                    f"({generic}) "
                    f"{profile['strength']} "
                    f"online."
                ),
        }
        
    @transaction.atomic
    def seed_product(
        self,
        profile,
    ):
        """
        Create or update a Product from a brand profile.
        """

        result = self.validate_profile(profile)

        if not result["valid"]:

            missing = ", ".join(result["missing"])

            self.errors.append(
                f'{profile["brand_name"]}: Missing {missing}'
            )

            self.skipped += 1

            return None

        brand = result["brand"]

        manufacturer = result["manufacturer"]

        category = result["category"]

        defaults = self.build_defaults(
            profile=profile,
            brand=brand,
            manufacturer=manufacturer,
        )

        product, created = (
            Product.objects.update_or_create(
                sku=profile["sku"],
                defaults=defaults,
            )
        )

        # ---------------------------------------------
        # Many-to-Many
        # ---------------------------------------------

        product.categories.set(
            [category]
        )

        # ---------------------------------------------
        # Statistics
        # ---------------------------------------------

        if created:

            self.created += 1

        else:

            self.updated += 1

        return product 

    # ---------------------------------------------------------
    # Main
    # ---------------------------------------------------------

    def seed(self):

        total = len(self.profiles)

        print()
        print("=" * 60)
        print("Product Seeder")
        print("=" * 60)

        for index, profile in enumerate(self.profiles, start=1):

            print(
                f"{index}/{total} -> "
                f'{profile["brand_name"]}'
            )

            try:

                self.seed_product(profile)

            except Exception as exc:

                self.errors.append(
                    f'{profile["brand_name"]}: {exc}'
                )

        print()
        print("Finished!")

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

            "total": len(self.profiles),

        }  

    def print_summary(self):

        print()

        print("=" * 60)
        print("Product Seeder Summary")
        print("=" * 60)

        print(f"Created : {self.created}")
        print(f"Updated : {self.updated}")
        print(f"Skipped : {self.skipped}")
        print(f"Errors  : {len(self.errors)}")
        print(f"Total   : {len(self.profiles)}")

        if self.errors:

            print()
            print("Error List")
            print("-" * 60)

            for error in self.errors:
                print(error)

        print("=" * 60) 

    def count(self):

        return len(self.profiles)    
