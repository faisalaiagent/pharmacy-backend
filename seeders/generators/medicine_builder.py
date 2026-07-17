"""
medicine_builder.py

Production-grade medicine builder.

This class assembles ONE complete medicine record from the
master datasets.

The builder itself DOES NOT write JSON and DOES NOT insert into
the database.

Responsibilities
----------------

Repository
    ↓

Randomizer
    ↓

Pricing Engine
    ↓

Manufacturer Mapper
    ↓

Brand Mapper
    ↓

SKU Generator
    ↓

Batch Generator
    ↓

Regulatory Generator
    ↓

Validator
    ↓

Dictionary Record
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from seeders.generators.medicine_repository import MedicineRepository
from seeders.generators.randomizer import Randomizer

from seeders.pricing_engine import PricingEngine
from seeders.matcher import Matcher

from seeders.sku_generator import SKUGenerator
from seeders.batch_generator import BatchGenerator
from seeders.regulatory import RegulatoryGenerator

from seeders.validators import ProductValidator


class MedicineBuilder:
    """
    Builds one medicine.

    Example

    builder = MedicineBuilder()

    medicine = builder.build()

    Returns

    dict
    """

    def __init__(

        self,

        repository: MedicineRepository | None = None,

        randomizer: Randomizer | None = None,

    ):

        # --------------------------------------------------
        # Core Dependencies
        # --------------------------------------------------

        self.repository = repository or MedicineRepository()

        self.random = randomizer or Randomizer()

        # --------------------------------------------------
        # Business Logic
        # --------------------------------------------------

        self.pricing = PricingEngine()

        self.matcher = Matcher()

        self.sku_generator = SKUGenerator()

        self.batch_generator = BatchGenerator()

        self.regulatory = RegulatoryGenerator()

        self.validator = ProductValidator()

        # --------------------------------------------------
        # Cached datasets
        # --------------------------------------------------

        self.categories = self.repository.categories()

        self.manufacturers = self.repository.manufacturers()

        self.generic_names = self.repository.generic_names()


        self.brands = self.repository.brands()

        self.therapeutic_classes = (
            self.repository.therapeutic_classes()
        )

        self.strengths = (
            self.repository.strengths()
        )

        self.dosage_forms = (
            self.repository.dosage_forms()
        )

        self.package_sizes = (
            self.repository.package_sizes()
        )

        self.indications = (
            self.repository.indications()
        )

        self.side_effects = (
            self.repository.side_effects()
        )

        self.contraindications = (
            self.repository.contraindications()
        )

        self.storage = (
            self.repository.storage()
        )

    # ============================================================
    # Helper Methods
    # ============================================================

    def random_item(
        self,
        dataset,
        default=None,
    ):
        """
        Safe random picker.
        """

        return self.random.choice(
            dataset,
            default=default,
        )

    def random_items(

        self,

        dataset,

        count=3,

        unique=True,

    ):
        """
        Returns multiple items.
        """

        return self.random.choices(

            dataset,

            k=count,

            unique=unique,

        )

    def lookup_brand(

        self,

        manufacturer_name,

    ):
        """
        Return a random brand
        belonging to a manufacturer.
        """

        candidates = [

            brand

            for brand in self.brands

            if brand.get("manufacturer") == manufacturer_name

        ]

        return self.random_item(candidates)

    def lookup_manufacturer(
        self,
        therapeutic_class=None,
    ):
        """
        Currently returns a random manufacturer.

        Future versions can map
        therapeutic classes
        to preferred manufacturers.
        """

        return self.random_item(
            self.manufacturers
        )

    def build_name(

        self,

        generic_name,

        strength,

        dosage_form,

    ):
        """
        Human-readable product title.
        """

        return (
            f"{generic_name} "
            f"{strength} "
            f"{dosage_form}"
        )

    def now(self):
        """
        UTC timestamp.
        """

        return datetime.utcnow()

    def decimal(
        self,
        value,
    ):
        """
        Force Decimal.
        """

        return Decimal(str(value))

    def normalize(
        self,
        text,
    ):
        """
        Normalize text.
        """

        if text is None:
            return ""

        return str(text).strip()

    def ensure_list(
        self,
        value,
    ):
        """
        Always returns list.
        """

        if value is None:
            return []

        if isinstance(
            value,
            list,
        ):
            return value

        return [value]

    def generate_codes(
        self,
        manufacturer,
        identity,
    ):
        """
        Generate SKU, batch and regulatory information.
        """

        manufacturer_name = ""

        if manufacturer:
            manufacturer_name = manufacturer.get("name", "")

        generic_name = identity.get("generic_name") or ""
        strength = identity.get("strength") or ""
        dosage_form = identity.get("dosage_form") or ""

        # --------------------------------------------------
        # SKU
        # --------------------------------------------------

        sku = self.sku_generator.generate(
            manufacturer_name=manufacturer_name,
            generic_name=generic_name,
            strength=strength,
            dosage_form=dosage_form,
        )

        # --------------------------------------------------
        # Batch Information
        # --------------------------------------------------

        batch = self.batch_generator.generate(
            manufacturer_name=manufacturer_name,
        )

        # --------------------------------------------------
        # Regulatory Information
        # --------------------------------------------------

        regulatory = self.regulatory.generate()

        # --------------------------------------------------
        # Merge Everything
        # --------------------------------------------------

        return {

            "sku": sku,

            "batch_number": batch["batch_number"],

            "lot_number": batch["lot_number"],

            "manufacturing_date": batch["manufacturing_date"],

            "expiry_date": batch["expiry_date"],

            "shelf_life_months": batch["shelf_life_months"],

            **regulatory,

        }
    # ============================================================
    # Internal validation
    # ============================================================

    def validate_record(
        self,
        record,
    ):
        """
        Pass record through
        project validator.
        """

        return self.validator.validate(
            record
        )

    # ============================================================
    # Debug
    # ============================================================

    def summary(self):
        """
        Useful while developing.
        """

        return {

            "categories":
                len(self.categories),

            "manufacturers":
                len(self.manufacturers),

            "brands":
                len(self.brands),

            "therapeutic_classes":
                len(self.therapeutic_classes),

            "strengths":
                len(self.strengths),

            "dosage_forms":
                len(self.dosage_forms),

            "package_sizes":
                len(self.package_sizes),

            "indications":
                len(self.indications),

            "side_effects":
                len(self.side_effects),

            "contraindications":
                len(self.contraindications),

            "storage":
                len(self.storage),

        }
# ============================================================
# SECTION 2
# Attribute Generation
# ============================================================

    def choose_category(self):
        """
        Select a category.
        """

        return self.random_item(self.categories)


    def choose_therapeutic_class(self):
        """
        Select a therapeutic class.
        """

        return self.random_item(self.therapeutic_classes)


    def choose_strength(self):
        """
        Select a medicine strength.
        """

        return self.random_item(self.strengths)


    def choose_dosage_form(self):
        """
        Tablet, Capsule, Syrup, Injection etc.
        """

        return self.random_item(self.dosage_forms)


    def choose_package_size(self):
        """
        Select package size.
        """

        return self.random_item(self.package_sizes)


    def choose_storage(self):
        """
        Storage instruction.
        """

        return self.random_item(self.storage)


    def choose_indications(self, minimum=2, maximum=5):
        """
        Clinical indications.
        """

        if not self.indications:
            return []

        count = self.random.randint(minimum, maximum)

        return self.random_items(
            self.indications,
            count=count,
    )


    def choose_side_effects(self, minimum=2, maximum=6):
        """
        Common adverse effects.
        """

        if not self.side_effects:
            return []

        count = self.random.randint(minimum, maximum)

        return self.random_items(
            self.side_effects,
            count=count,
    )


    def choose_contraindications(self, minimum=1, maximum=3):
        """
        Contraindications.
        """

        if not self.contraindications:
            return []

        count = self.random.randint(minimum, maximum)

        return self.random_items(
            self.contraindications,
            count=count,
    )


# ------------------------------------------------------------
# Composite Attribute Builder
# ------------------------------------------------------------

    def generate_attributes(self):
        """
        Generates all pharmaceutical attributes.
        """

        category = self.choose_category()

        therapeutic = self.choose_therapeutic_class()

        dosage_form = self.choose_dosage_form()

        strength = self.choose_strength()

        package = self.choose_package_size()

        storage = self.choose_storage()

        indications = self.choose_indications()

        side_effects = self.choose_side_effects()

        contraindications = self.choose_contraindications()

        return {

            "category": category,

            "therapeutic_class": therapeutic,

            "dosage_form": dosage_form,

            "strength": strength,

            "package_size": package,

            "storage": storage,

            "indications": indications,

            "side_effects": side_effects,

            "contraindications": contraindications,

        }


    # ------------------------------------------------------------
    # Generic Medicine Name Builder
    # ------------------------------------------------------------

    def build_generic_name(self):
            """
            Select a generic medicine from generic_names.json.
            """

            if not self.generic_names:
                return "Unknown Medicine"

            item = self.random.choice(self.generic_names)

            if isinstance(item, dict):
                return item.get("generic_name", "Unknown Medicine")

            if isinstance(item, str):
                return item

            return "Unknown Medicine"


    # ------------------------------------------------------------
    # Medicine Identity
    # ------------------------------------------------------------

    def generate_identity(self):
        """
        Generate the core identity of a medicine.

        Returns
        -------
        dict
        """

        generic_name = self.build_generic_name()

        dosage = self.choose_dosage_form()

        strength = self.choose_strength()

        product_name = self.build_name(
            generic_name,
            strength,
            dosage,
        )

        identity = {

            # Required by ProductValidator
            "name": product_name,

            # Useful internal/display field
            "product_name": product_name,

            # Generic information
            "generic_name": generic_name,

            "strength": strength,

            "dosage_form": dosage,

        }

        # Temporary debug output
        print("\nIDENTITY:")
        print(identity)

        return identity
    # ============================================================
    # SECTION 3
    # Commercial Product Generation
    # ============================================================

    def assign_manufacturer(self, therapeutic_class=None):
        """
        Select a manufacturer.

        Future versions can use therapeutic-class
        mapping for smarter assignments.
        """

        manufacturer = self.lookup_manufacturer(
            therapeutic_class=therapeutic_class
        )

        if manufacturer is None:
            return {}

        return manufacturer


    def assign_brand(self, manufacturer):
        """
        Select one brand belonging to the manufacturer.
        """

        if not manufacturer:
            return {}

        manufacturer_name = manufacturer.get("name")

        brand = self.lookup_brand(
            manufacturer_name
        )

        if brand is None:

            return {

                "name": manufacturer_name,

                "manufacturer": manufacturer_name,

            }

        return brand


    # ------------------------------------------------------------
    # Pricing
    # ------------------------------------------------------------

    def generate_pricing(
        self,
        dosage_form,
        strength,
    ):
        """
        Generate realistic Pakistani market pricing.
        """

        try:

            price = self.pricing.generate_price(
                dosage_form=dosage_form,
                strength=strength,
            )

        except Exception:

            price = self.random.decimal(
                60,
                2500,
            )

        # ----------------------------------------------------
        # Cost Price (typically 65–85% of retail)
        # ----------------------------------------------------

        margin = Decimal(
            str(
                self.random.randint(
                    65,
                    85,
                )
            )
        ) / Decimal("100")

        cost_price = (
            price * margin
        ).quantize(
            Decimal("0.01")
        )

        # ----------------------------------------------------
        # Optional Discount
        # ----------------------------------------------------

        discount = Decimal("0.00")

        sale_price = price

        if self.random.chance(35):

            discount = Decimal(
                str(
                    self.random.randint(
                        5,
                        20,
                    )
                )
            )

            sale_price = (
                price
                -
                (
                    price
                    * discount
                    / Decimal("100")
                )
            ).quantize(
                Decimal("0.01")
            )

        return {

            "price": price,

            "cost_price": cost_price,

            "sale_price": sale_price,

            "discount_percent": discount,

            "currency": "PKR",

        }


    # ------------------------------------------------------------
    # Commercial Codes
    # ------------------------------------------------------------

    def generate_identifiers(
        self,
        manufacturer,
        identity,
    ):
        """
        Generate identifiers used by the product.
        """

        codes = self.generate_codes(
            manufacturer,
            identity,
        )

        return {

            "sku": codes["sku"],

            "batch_number": codes["batch_number"],

            "lot_number": codes["lot_number"],

            "manufacturing_date": codes["manufacturing_date"],

            "expiry_date": codes["expiry_date"],

            "shelf_life_months": codes["shelf_life_months"],

            "regulatory_number": codes["regulatory_approval_number"],

            "registration_id": codes["registration_id"],

            "approval_status": codes["approval_status"],

            "approval_date": codes["approval_date"],

            "renewal_date": codes["renewal_date"],

        }


    # ------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------

    def generate_inventory(self):
        """
        Default inventory values.
        """

        stock = self.random.randint(
            20,
            500,
        )

        reorder = max(

            10,

            stock // 5,

        )

        return {

            "stock_quantity": stock,

            "reorder_level": reorder,

            "is_in_stock": stock > 0,

            "track_inventory": True,

        }


    # ------------------------------------------------------------
    # Product Status
    # ------------------------------------------------------------

    def generate_status(self):

        return {

            "is_active": True,

            "is_featured":
                self.random.chance(10),

            "is_prescription":
                self.random.chance(45),

            "is_refundable":
                True,

            "is_taxable":
                True,

        }


    # ------------------------------------------------------------
    # SEO
    # ------------------------------------------------------------

    def generate_seo(
        self,
        product_name,
    ):

        return {

            "meta_title":
                product_name,

            "meta_description":

                f"Buy {product_name} online in Pakistan.",

            "keywords": [

                product_name,

                "medicine",

                "pharmacy",

                "Pakistan",

            ],

        }


    # ------------------------------------------------------------
    # Image Metadata
    # ------------------------------------------------------------

    def generate_media(
        self,
        product_name,
    ):

        slug = (

            product_name

            .lower()

            .replace(" ", "-")

        )

        return {

            "image":

                f"/media/products/{slug}.jpg",

            "thumbnail":

                f"/media/products/{slug}_thumb.jpg",

            "gallery": [],

        }


    # ------------------------------------------------------------
    # Manufacturer + Brand Package
    # ------------------------------------------------------------

    def generate_company_information(
        self,
        therapeutic_class=None,
    ):

        manufacturer = self.assign_manufacturer(
            therapeutic_class
        )

        brand = self.assign_brand(
            manufacturer
        )

        return {

            "manufacturer": manufacturer,

            "brand": brand,

        }


    # ------------------------------------------------------------
    # Commercial Block
    # ------------------------------------------------------------

    def generate_commercial_data(
        self,
        identity,
        attributes,
    ):
        """
        Complete commercial metadata.
        """

        company = self.generate_company_information(

            attributes.get(
                "therapeutic_class"
            )

        )

        identifiers = self.generate_identifiers(

            company["manufacturer"],

            identity,

        )

        pricing = self.generate_pricing(

            identity["dosage_form"],

            identity["strength"],

        )

        inventory = self.generate_inventory()

        status = self.generate_status()

        seo = self.generate_seo(

            identity["product_name"]

        )

        media = self.generate_media(

            identity["product_name"]

        )

        return {

            **company,

            **pricing,

            **identifiers,

            **inventory,

            **status,

            **seo,

            **media,

        }
    # ============================================================
    # SECTION 4
    # Record Assembly
    # ============================================================

    def assemble_record(
        self,
        identity,
        attributes,
        commercial,
    ):
        """
        Merge all generated blocks into a single medicine record.
        """

        record = {

            # --------------------------------------------------
            # Identity
            # --------------------------------------------------

            **identity,

            # --------------------------------------------------
            # Medical Attributes
            # --------------------------------------------------

            **attributes,

            # --------------------------------------------------
            # Commercial
            # --------------------------------------------------

            **commercial,

            # --------------------------------------------------
            # Metadata
            # --------------------------------------------------

            "country": "Pakistan",

            "language": "en",

            "source": "AI Pharmacy Generator",

            "generated_at": self.now().isoformat(),

            "version": 1,

        }

        return record
        print("\nIDENTITY BLOCK")
        print(identity)

        print("\nFINAL RECORD KEYS")
        print(sorted(record.keys()))

    # ============================================================
    # Validation
    # ============================================================

    def validate(self, record):
        """
        Validate generated medicine.
        """

        try:

            self.validate_record(record)

            return record

        except Exception as exc:

            print()

            print("Validation Failed")

            print(exc)

            print()

            return None


    # ============================================================
    # Export Helper
    # ============================================================

    def export_ready(self, record):
        """
        Flatten record if required.

        Currently returns record unchanged.

        Future versions may flatten nested
        manufacturer / brand objects.
        """

        return record


    # ============================================================
    # Public Builder
    # ============================================================

    def build(self):
        """
        Build ONE medicine.

        Returns
        -------
        dict
        """

        # -------------------------------
        # Identity
        # -------------------------------

        identity = self.generate_identity()

        # -------------------------------
        # Attributes
        # -------------------------------

        attributes = self.generate_attributes()

        # -------------------------------
        # Commercial
        # -------------------------------

        commercial = self.generate_commercial_data(

            identity,

            attributes,

        )

        # -------------------------------
        # Merge Everything
        # -------------------------------

        record = self.assemble_record(

            identity,

            attributes,

            commercial,

        )

        # -------------------------------
        # Validate
        # -------------------------------

        record = self.validate(record)

        if record is None:

            return None

        # -------------------------------
        # Export Formatting
        # -------------------------------

        return self.export_ready(record)


    # ============================================================
    # Bulk Builder
    # ============================================================

    def build_many(
        self,
        count=1000,
    ):
        """
        Build multiple medicines.
        """

        medicines = []

        for _ in range(count):

            medicine = self.build()

            if medicine:

                medicines.append(medicine)

        return medicines    