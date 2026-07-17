from __future__ import annotations

import json
import random

from copy import deepcopy
from pathlib import Path

from .base_generator import BaseGenerator

from ..repositories.brand_repository import (
    BrandRepository,
)

from ..repositories.manufacturer_repository import (
    ManufacturerRepository,
)

from ..repositories.medicine_profile_repository import (
    MedicineProfileRepository,
)

class BrandProfileGenerator(
    BaseGenerator
):
    """
    Generates brand product profiles.
    """

    OUTPUT_FILE = (
        "brand_profiles.json"
    )

    def __init__(self):

        super().__init__()

        self.brand_repo = (
            BrandRepository()
        )

        self.manufacturer_repo = (
            ManufacturerRepository()
        )

        self.medicine_repo = (
            MedicineProfileRepository()
        )

        self._profiles = []

    PRICE_RANGES = {

    "Pain Relief": (40, 250),

    "Antibiotics": (150, 900),

    "Heart Care": (200, 1200),

    "Diabetes": (250, 1500),

    "Respiratory": (300, 2000),

    "Gastrointestinal": (150, 800),

    "Vitamins": (150, 2500),

}
    STATUS_OPTIONS = [

    "active",

]
    CURRENCY = "PKR"

    def build_sku(
        self,
        manufacturer,
        generic,
        strength,
        dosage_form,
        sequence,
    ):

        mfg = manufacturer[:3].upper()

        gen = generic[:3].upper()

        strength_code = (
            strength
            .replace("mg", "")
            .replace("mcg", "")
            .replace("IU", "")
        )

        dosage = dosage_form[:3].upper()

        return (

            f"{mfg}-"

            f"{gen}-"

            f"{strength_code}-"

            f"{dosage}-"

            f"{sequence:03d}"

        )    
    
    def generate_price(
        self,
        category,
    ):

        minimum, maximum = (

            self.PRICE_RANGES.get(
                category,
                (100, 500),
            )

        )

        return random.randint(
            minimum,
            maximum,
        )

    def prescription_required(
        self,
        category,
    ):

        prescription_categories = {

            "Antibiotics",

            "Heart Care",

            "Diabetes",

        }

        return (
            category
            in prescription_categories
        )
    
    def build_profile(
        self,
        brand: dict,
        sequence: int,
    ):
        """
        Builds one complete brand profile.
        """

        generic_name = brand["generic_name"]

        medicine = self.medicine_repo.get(
            generic_name
        )

        if medicine is None:

            raise ValueError(
                f"Medicine profile not found: {generic_name}"
            )

        profile = deepcopy(medicine)

        manufacturer = brand["manufacturer"]

        strength = random.choice(
            profile["strengths"]
        )

        dosage_form = random.choice(
            profile["dosage_forms"]
        )

        package_size = random.choice(
            profile["package_sizes"]
        )

        profile.update({

            "sku": self.build_sku(
                manufacturer,
                generic_name,
                strength,
                dosage_form,
                sequence,
            ),

            "brand_name": brand["name"],

            "manufacturer": manufacturer,

            "strength": strength,

            "dosage_form": dosage_form,

            "package_size": package_size,

            "price": self.generate_price(
                profile["category"]
            ),

            "currency": self.CURRENCY,

            "prescription_required":
                self.prescription_required(
                    profile["category"]
                ),

            "status": random.choice(
                self.STATUS_OPTIONS
            ),

        })

        return profile
    
    def build_profiles(self):
        """
        Builds brand profiles for all brands.

        Returns
        -------
        list[dict]
        """

        profiles = []

        for sequence, brand in enumerate(
            self.brand_repo.brands,
            start=1,
        ):

            profile = self.build_profile(
                brand=brand,
                sequence=sequence,
            )

            profiles.append(
                profile
            )

        self._profiles = deepcopy(
            profiles
        )

        return profiles
    
    def validate_profiles(
        self,
        profiles,
    ):
        """
        Validates generated brand profiles.

        Returns
        -------
        list[dict]
        """

        skus = set()

        brand_names = set()

        required_fields = [

            "sku",

            "brand_name",

            "generic_name",

            "manufacturer",

            "category",

            "therapeutic_class",

            "strength",

            "dosage_form",

            "package_size",

            "price",

            "currency",

            "prescription_required",

            "status",

        ]

        for profile in profiles:

            # --------------------------------------------
            # Required fields
            # --------------------------------------------

            for field in required_fields:

                if field not in profile:

                    raise ValueError(
                        f"Missing '{field}' in "
                        f"{profile.get('brand_name', 'Unknown')}"
                    )

            # --------------------------------------------
            # Unique SKU
            # --------------------------------------------

            sku = profile["sku"]

            if sku in skus:

                raise ValueError(
                    f"Duplicate SKU: {sku}"
                )

            skus.add(sku)

            # --------------------------------------------
            # Unique Brand Name
            # --------------------------------------------

            brand_name = profile["brand_name"]

            if brand_name in brand_names:

                raise ValueError(
                    f"Duplicate brand: {brand_name}"
                )

            brand_names.add(brand_name)

            # --------------------------------------------
            # Price Validation
            # --------------------------------------------

            if profile["price"] <= 0:

                raise ValueError(
                    f"{brand_name} has invalid price."
                )

            # --------------------------------------------
            # Strength
            # --------------------------------------------

            if not profile["strength"]:

                raise ValueError(
                    f"{brand_name} has no strength."
                )

            # --------------------------------------------
            # Dosage Form
            # --------------------------------------------

            if not profile["dosage_form"]:

                raise ValueError(
                    f"{brand_name} has no dosage form."
                )

            # --------------------------------------------
            # Package Size
            # --------------------------------------------

            if not profile["package_size"]:

                raise ValueError(
                    f"{brand_name} has no package size."
                )

        return profiles
    
    def generate(self):
        """
        Generates all brand product profiles.

        Returns
        -------
        list[dict]
        """

        profiles = self.build_profiles()

        profiles = self.validate_profiles(
            profiles
        )

        self._profiles = deepcopy(
            profiles
        )

        return profiles