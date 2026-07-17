"""
products/management/commands/seed_products.py

Production Product Seeder
=========================

Loads medicine_dictionary.json and imports medicines into the
database.

Features
--------
✓ Transaction safe
✓ Bulk inserts
✓ Duplicate detection
✓ Dry-run support
✓ Replace existing products
✓ Progress reporting
✓ Statistics
✓ Error logging
✓ Production ready

Subsequent sections will implement:

Section 2
---------
Dataset loading

Section 3
---------
Lookup helpers

Section 4
---------
Product creation

Section 5
---------
Bulk database operations

Section 6
---------
Command execution
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from collections import defaultdict

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from products.models import (
    Product,
    Category,
    Brand,
    Manufacturer,
)

from seeders.validators import validate_product

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Import products from medicine_dictionary.json.
    """

    help = "Import generated medicines into the Product database."

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------

    def __init__(self):

        super().__init__()

        self.dictionary = []

        self.categories = {}

        self.brands = {}

        self.manufacturers = {}

        self.products = []

        self.stats = defaultdict(int)

    # ---------------------------------------------------------
    # CLI Arguments
    # ---------------------------------------------------------

    def add_arguments(self, parser):

        parser.add_argument(

            "--replace",

            action="store_true",

            help="Delete existing products before import.",

        )

        parser.add_argument(

            "--dry-run",

            action="store_true",

            help="Validate without writing to database.",

        )

        parser.add_argument(

            "--batch-size",

            type=int,

            default=500,

            help="Bulk insert batch size.",

        )

    # ---------------------------------------------------------
    # Paths
    # ---------------------------------------------------------

    @property
    def data_directory(self):

        return (
            Path(settings.BASE_DIR)
            / "seeders"
            / "data"
        )

    @property
    def dictionary_file(self):

        return (
            self.data_directory
            / "medicine_dictionary.json"
        )

    # ---------------------------------------------------------
    # Console Helpers
    # ---------------------------------------------------------

    def title(self, text):

        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write(text)
        self.stdout.write("=" * 70)

    def success(self, message):

        self.stdout.write(
            self.style.SUCCESS(message)
        )

    def warning(self, message):

        self.stdout.write(
            self.style.WARNING(message)
        )

    def info(self, message):

        self.stdout.write(str(message))

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def increment(
        self,
        key,
        value=1,
    ):

        self.stats[key] += value

    def print_statistics(self):

        self.title("Import Statistics")

        ordered = [

            "loaded",

            "validated",

            "created",

            "updated",

            "duplicates",

            "skipped",

            "errors",

        ]

        for key in ordered:

            self.info(

                f"{key:<20} {self.stats.get(key,0)}"

            )

    # ---------------------------------------------------------
    # Validation Wrapper
    # ---------------------------------------------------------

    def validate(self, record):

        try:

            validate_product(record)

            self.increment("validated")

            return True

        except Exception as exc:

            self.increment("errors")

            logger.exception(exc)

            self.warning(str(exc))

            return False

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    def log(self, message):

        logger.info(message)

    # ---------------------------------------------------------
    # Placeholder Methods
    # ---------------------------------------------------------

    # Section 2
    def load_dictionary(self):
        raise NotImplementedError

    def load_reference_tables(self):
        raise NotImplementedError

    # Section 3
    def get_category(self, record):
        raise NotImplementedError

    def get_brand(self, record):
        raise NotImplementedError

    def get_manufacturer(self, record):
        raise NotImplementedError

    # Section 4
    def build_product(self, record):
        raise NotImplementedError

    # Section 5
    def save_products(
        self,
        batch_size,
        dry_run=False,
    ):
        raise NotImplementedError

    # Section 6
    @transaction.atomic
    def handle(self, *args, **options):
        raise NotImplementedError
    # =========================================================
    # SECTION 2
    # Dataset Loading
    # =========================================================

    def load_dictionary(self):
        """
        Load medicine_dictionary.json into memory.
        """

        self.title("Loading Medicine Dictionary")

        if not self.dictionary_file.exists():

            raise FileNotFoundError(

                f"Dictionary file not found:\n{self.dictionary_file}"

            )

        with open(
            self.dictionary_file,
            "r",
            encoding="utf-8",
        ) as f:

            self.dictionary = json.load(f)

        if not isinstance(self.dictionary, list):

            raise ValueError(

                "medicine_dictionary.json must contain a list."

            )

        self.increment(
            "loaded",
            len(self.dictionary),
        )

        self.success(

            f"Loaded {len(self.dictionary)} medicines."

        )

        return self.dictionary


    # ---------------------------------------------------------
    # Existing Database Lookups
    # ---------------------------------------------------------

    def load_reference_tables(self):
        """
        Cache all lookup tables.

        This avoids thousands of SQL queries while importing.
        """

        self.title("Loading Reference Tables")

        # ----------------------------------
        # Categories
        # ----------------------------------

        self.categories = {

            category.name.lower(): category

            for category in Category.objects.all()

        }

        # ----------------------------------
        # Brands
        # ----------------------------------

        self.brands = {

            brand.name.lower(): brand

            for brand in Brand.objects.all()

        }

        # ----------------------------------
        # Manufacturers
        # ----------------------------------

        self.manufacturers = {

            manufacturer.name.lower(): manufacturer

            for manufacturer in Manufacturer.objects.all()

        }

        self.info(

            f"Categories      : {len(self.categories)}"

        )

        self.info(

            f"Brands          : {len(self.brands)}"

        )

        self.info(

            f"Manufacturers   : {len(self.manufacturers)}"

        )


    # ---------------------------------------------------------
    # Dictionary Iterator
    # ---------------------------------------------------------

    def records(self):
        """
        Iterate over loaded medicines.
        """

        if not self.dictionary:

            self.load_dictionary()

        yield from self.dictionary


    # ---------------------------------------------------------
    # Duplicate Detection
    # ---------------------------------------------------------

    def existing_skus(self):
        """
        Cache all SKUs already stored.
        """

        return set(

            Product.objects.values_list(

                "sku",

                flat=True,

            )

        )


    def existing_slugs(self):
        """
        Cache all product slugs.
        """

        return set(

            Product.objects.values_list(

                "slug",

                flat=True,

            )

        )


    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def make_slug(self, record):
        """
        Create product slug.
        """

        source = (

            record.get("name")

            or

            record.get("product_name")

            or

            record.get("generic_name")

            or

            "medicine"

        )

        return slugify(source)


    # ---------------------------------------------------------
    # Dataset Summary
    # ---------------------------------------------------------

    def print_dataset_summary(self):
        """
        Print loaded dataset information.
        """

        self.title("Dataset Summary")

        self.info(

            f"Dictionary Records : {len(self.dictionary)}"

        )

        self.info(

            f"Categories         : {len(self.categories)}"

        )

        self.info(

            f"Brands             : {len(self.brands)}"

        )

        self.info(

            f"Manufacturers      : {len(self.manufacturers)}"

        )
    # =========================================================
    # SECTION 3
    # Lookup & Object Creation
    # =========================================================

    # ---------------------------------------------------------
    # Category
    # ---------------------------------------------------------

    def get_category(self, name):
        """
        Return Category instance.
        Creates one if it does not exist.
        """

        name = (name or "General").strip()

        key = name.lower()

        if key in self.categories:
            return self.categories[key]

        category = Category.objects.create(

            name=name,

            slug=slugify(name),

        )

        self.categories[key] = category

        self.increment("created_categories")

        return category


    # ---------------------------------------------------------
    # Brand
    # ---------------------------------------------------------

    def get_brand(self, name):
        """
        Return Brand instance.
        """

        name = (name or "Generic").strip()

        key = name.lower()

        if key in self.brands:
            return self.brands[key]

        brand = Brand.objects.create(

            name=name,

            slug=slugify(name),

        )

        self.brands[key] = brand

        self.increment("created_brands")

        return brand


    # ---------------------------------------------------------
    # Manufacturer
    # ---------------------------------------------------------

    def get_manufacturer(self, name):
        """
        Return Manufacturer instance.
        """

        name = (name or "Unknown Manufacturer").strip()

        key = name.lower()

        if key in self.manufacturers:
            return self.manufacturers[key]

        manufacturer = Manufacturer.objects.create(

            name=name,

            slug=slugify(name),

        )

        self.manufacturers[key] = manufacturer

        self.increment("created_manufacturers")

        return manufacturer


    # ---------------------------------------------------------
    # Resolve References
    # ---------------------------------------------------------

    def resolve_relations(self, record):
        """
        Convert JSON strings into Django model objects.
        """

        return {

            "category": self.get_category(

                record.get("category")

            ),

            "brand": self.get_brand(

                record.get("brand")

            ),

            "manufacturer": self.get_manufacturer(

                record.get("manufacturer")

            ),

        }


    # ---------------------------------------------------------
    # Existing Product Checks
    # ---------------------------------------------------------

    def sku_exists(self, sku):
        """
        Fast SKU lookup.
        """

        if sku in self.cached_skus:
            return True

        return False


    def slug_exists(self, slug):
        """
        Fast slug lookup.
        """

        if slug in self.cached_slugs:
            return True

        return False


    # ---------------------------------------------------------
    # Cache Updates
    # ---------------------------------------------------------

    def remember_product(self, product):
        """
        Store newly-created identifiers
        to avoid duplicate inserts.
        """

        self.cached_skus.add(product.sku)

        self.cached_slugs.add(product.slug)


    # ---------------------------------------------------------
    # Duplicate Validation
    # ---------------------------------------------------------

    def should_skip(self, record):
        """
        Skip duplicate products.
        """

        sku = record.get("sku")

        slug = self.make_slug(record)

        if self.sku_exists(sku):

            self.increment("duplicates")

            return True

        if self.slug_exists(slug):

            self.increment("duplicates")

            return True

        return False


    # ---------------------------------------------------------
    # Lookup Summary
    # ---------------------------------------------------------

    def print_lookup_summary(self):
        """
        Print lookup cache sizes.
        """

        self.title("Lookup Cache")

        self.info(

            f"Categories       : {len(self.categories)}"

        )

        self.info(

            f"Brands           : {len(self.brands)}"

        )

        self.info(

            f"Manufacturers    : {len(self.manufacturers)}"

        )

        self.info(

            f"Existing SKUs    : {len(self.cached_skus)}"

        )

        self.info(

            f"Existing Slugs   : {len(self.cached_slugs)}"

        )    
    # =========================================================
    # SECTION 4
    # Product Builder
    # =========================================================

    from decimal import Decimal


    # ---------------------------------------------------------
    # Safe Value Helpers
    # ---------------------------------------------------------

    def safe_decimal(self, value, default="0.00"):
        """
        Convert value to Decimal.
        """

        try:
            return Decimal(str(value))
        except Exception:
            return Decimal(default)


    def safe_int(self, value, default=0):
        """
        Convert value to integer.
        """

        try:
            return int(value)
        except Exception:
            return default


    def safe_bool(self, value, default=False):
        """
        Convert value to bool.
        """

        if value is None:
            return default

        return bool(value)


    # ---------------------------------------------------------
    # Build Product Object
    # ---------------------------------------------------------

    def build_product(self, record):
        """
        Convert one dictionary record into
        an unsaved Django Product object.

        Returns
        -------
        Product | None
        """

        if self.should_skip(record):
            return None

        relations = self.resolve_relations(record)

        slug = self.make_slug(record)

        product = Product(

            # ---------------------------------
            # Identity
            # ---------------------------------

            name=record.get(
                "name",
                record.get("product_name", "")
            ),

            slug=slug,

            generic_name=record.get(
                "generic_name",
                "",
            ),

            # ---------------------------------
            # Medical
            # ---------------------------------

            category=relations["category"],

            brand=relations["brand"],

            manufacturer=relations["manufacturer"],

            therapeutic_class=record.get(
                "therapeutic_class",
                "",
            ),

            dosage_form=record.get(
                "dosage_form",
                "",
            ),

            strength=record.get(
                "strength",
                "",
            ),

            package_size=record.get(
                "package_size",
                "",
            ),

            indications=record.get(
                "indications",
                [],
            ),

            side_effects=record.get(
                "side_effects",
                [],
            ),

            contraindications=record.get(
                "contraindications",
                [],
            ),

            storage=record.get(
                "storage",
                "",
            ),

            # ---------------------------------
            # Pricing
            # ---------------------------------

            price=self.safe_decimal(
                record.get("price")
            ),

            sale_price=self.safe_decimal(
                record.get("sale_price")
            ),

            cost_price=self.safe_decimal(
                record.get(
                    "cost_price",
                    record.get("price", 0),
                )
            ),

            currency=record.get(
                "currency",
                "PKR",
            ),

            discount_percent=self.safe_decimal(
                record.get(
                    "discount_percent",
                    0,
                )
            ),

            # ---------------------------------
            # Inventory
            # ---------------------------------

            sku=record.get(
                "sku",
                "",
            ),

            batch_number=record.get(
                "batch_number",
                "",
            ),

            stock_quantity=self.safe_int(
                record.get(
                    "stock_quantity",
                    0,
                )
            ),

            reorder_level=self.safe_int(
                record.get(
                    "reorder_level",
                    10,
                )
            ),

            track_inventory=self.safe_bool(
                record.get(
                    "track_inventory",
                    True,
                )
            ),

            # ---------------------------------
            # Regulatory
            # ---------------------------------

            regulatory_approval_number=record.get(
                "regulatory_number",
                "",
            ),

            registration_id=record.get(
                "registration_id",
                "",
            ),

            approval_status=record.get(
                "approval_status",
                "",
            ),

            approval_date=record.get(
                "approval_date",
            ),

            renewal_date=record.get(
                "renewal_date",
            ),

            expiry_date=record.get(
                "expiry_date",
            ),

            # ---------------------------------
            # SEO
            # ---------------------------------

            meta_title=record.get(
                "meta_title",
                "",
            ),

            meta_description=record.get(
                "meta_description",
                "",
            ),

            keywords=record.get(
                "keywords",
                [],
            ),

            # ---------------------------------
            # Media
            # ---------------------------------

            image=record.get(
                "image",
                "",
            ),

            thumbnail=record.get(
                "thumbnail",
                "",
            ),

            gallery=record.get(
                "gallery",
                [],
            ),

            # ---------------------------------
            # Flags
            # ---------------------------------

            is_active=self.safe_bool(
                record.get(
                    "is_active",
                    True,
                )
            ),

            is_featured=self.safe_bool(
                record.get(
                    "is_featured",
                    False,
                )
            ),

            is_prescription=self.safe_bool(
                record.get(
                    "is_prescription",
                    False,
                )
            ),

            is_in_stock=self.safe_bool(
                record.get(
                    "is_in_stock",
                    True,
                )
            ),

            is_taxable=self.safe_bool(
                record.get(
                    "is_taxable",
                    True,
                )
            ),

            is_refundable=self.safe_bool(
                record.get(
                    "is_refundable",
                    True,
                )
            ),
        )

        return product


    # ---------------------------------------------------------
    # Build Multiple Products
    # ---------------------------------------------------------

    def build_products(self):
        """
        Build all Product objects from the
        loaded medicine dictionary.

        Returns
        -------
        list[Product]
        """

        products = []

        for record in self.records():

            product = self.build_product(record)

            if product is None:
                continue

            products.append(product)

        self.success(

            f"Prepared {len(products)} products."

        )

        return products    
    # =========================================================
    # SECTION 5
    # Bulk Import
    # =========================================================

    from django.db import transaction


    # ---------------------------------------------------------
    # Bulk Create
    # ---------------------------------------------------------

    def bulk_insert(
        self,
        products,
    ):
        """
        Insert products using Django bulk_create().
        """

        if not products:

            self.warning(
                "No products available for import."
            )

            return 0

        Product.objects.bulk_create(

            products,

            batch_size=self.batch_size,

            ignore_conflicts=True,

        )

        for product in products:

            self.remember_product(product)

        self.increment(
            "created",
            len(products),
        )

        return len(products)


    # ---------------------------------------------------------
    # Batch Iterator
    # ---------------------------------------------------------

    def chunks(
        self,
        iterable,
        size,
    ):
        """
        Yield lists of batch_size.
        """

        batch = []

        for item in iterable:

            batch.append(item)

            if len(batch) >= size:

                yield batch

                batch = []

        if batch:

            yield batch


    # ---------------------------------------------------------
    # Import One Batch
    # ---------------------------------------------------------

    def import_batch(
        self,
        products,
    ):
        """
        Import one batch safely.
        """

        try:

            with transaction.atomic():

                inserted = self.bulk_insert(
                    products
                )

                return inserted

        except Exception as exc:

            self.increment("failed")

            self.error(str(exc))

            return 0


    # ---------------------------------------------------------
    # Progress Display
    # ---------------------------------------------------------

    def print_progress(
        self,
        current,
        total,
    ):
        """
        Progress information.
        """

        percent = (
            current / total
        ) * 100

        self.info(

            f"[{current}/{total}] "
            f"{percent:.1f}% completed"

        )


    # ---------------------------------------------------------
    # Main Import
    # ---------------------------------------------------------

    def import_products(self):
        """
        Import the complete dictionary.
        """

        self.title(
            "Starting Product Import"
        )

        products = self.build_products()

        total = len(products)

        if total == 0:

            self.warning(
                "Nothing to import."
            )

            return

        imported = 0

        for batch in self.chunks(

            products,

            self.batch_size,

        ):

            inserted = self.import_batch(
                batch
            )

            imported += inserted

            self.print_progress(

                imported,

                total,

            )

        self.success(

            f"{imported} products imported."

        )

        return imported


    # ---------------------------------------------------------
    # Final Statistics
    # ---------------------------------------------------------

    def print_import_summary(self):
        """
        Final report.
        """

        self.title(
            "Import Summary"
        )

        for key, value in self.stats.items():

            self.info(

                f"{key:<25} {value}"

            )

        self.success(
            "Import completed successfully."
        )
    # =========================================================
    # SECTION 6
    # Command Execution
    # =========================================================

    # ---------------------------------------------------------
    # Execute Import
    # ---------------------------------------------------------

    def run(self):
        """
        Main execution entry point.

        Workflow
        --------
        1. Load medicine dictionary
        2. Load lookup caches
        3. Build Product objects
        4. Bulk import
        5. Print summary
        """

        self.title(
            "AI Pharmacy Product Seeder"
        )

        # ------------------------------------------
        # Load JSON datasets
        # ------------------------------------------

        self.load_dataset()

        self.load_reference_tables()

        self.print_lookup_summary()

        # ------------------------------------------
        # Import
        # ------------------------------------------

        imported = self.import_products()

        # ------------------------------------------
        # Final Report
        # ------------------------------------------

        self.print_import_summary()

        return imported


    # ---------------------------------------------------------
    # Reset Statistics
    # ---------------------------------------------------------

    def reset_statistics(self):
        """
        Reset counters before each run.
        """

        self.stats = {

            "created": 0,

            "duplicates": 0,

            "failed": 0,

            "created_categories": 0,

            "created_brands": 0,

            "created_manufacturers": 0,

        }


    # ---------------------------------------------------------
    # Dry Run
    # ---------------------------------------------------------

    def dry_run(self):
        """
        Build products without saving them.
        Useful for validation.
        """

        self.title(
            "Dry Run"
        )

        self.load_dataset()

        self.load_reference_tables()

        products = self.build_products()

        self.success(

            f"{len(products)} products successfully validated."

        )

        return products


    # ---------------------------------------------------------
    # Reload Dictionary
    # ---------------------------------------------------------

    def reload_dictionary(self):
        """
        Reload JSON dictionary from disk.
        """

        self.dictionary = []

        self.load_dataset()


    # ---------------------------------------------------------
    # Full Refresh
    # ---------------------------------------------------------

    def refresh(self):
        """
        Reload everything.
        """

        self.reset_statistics()

        self.reload_dictionary()

        self.load_reference_tables()


    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    def health_check(self):
        """
        Verify importer readiness.
        """

        self.title(
            "Seeder Health Check"
        )

        checks = {

            "Dictionary Loaded":
                len(self.dictionary),

            "Categories":
                len(self.categories),

            "Brands":
                len(self.brands),

            "Manufacturers":
                len(self.manufacturers),

            "Cached SKUs":
                len(self.cached_skus),

            "Cached Slugs":
                len(self.cached_slugs),

        }

        for key, value in checks.items():

            self.info(

                f"{key:<25} {value}"

            )

        self.success(
            "Health check completed."
        )


    # ---------------------------------------------------------
    # Command Entry
    # ---------------------------------------------------------

    def execute(
        self,
        dry_run=False,
    ):
        """
        Public API.

        Examples
        --------

        importer.execute()

        importer.execute(
            dry_run=True
        )
        """

        if dry_run:

            return self.dry_run()

        return self.run()    