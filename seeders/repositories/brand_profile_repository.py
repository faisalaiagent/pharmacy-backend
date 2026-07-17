from __future__ import annotations

import json
import random

from copy import deepcopy
from collections import defaultdict, Counter
from pathlib import Path

class BrandProfileRepository:
    """
    Repository for generated brand product profiles.

    Loads brand_profiles.json and provides
    fast lookup utilities.
    """

    DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "brand_profiles.json"
)
    
    def __init__(self):

        self._profiles = self._load()

        self._validate()

        self._brand_index = {}

        self._generic_index = defaultdict(list)

        self._manufacturer_index = defaultdict(list)

        self._category_index = defaultdict(list)

        self._sku_index = {}

        self._build_indexes()

    def _load(self):

        with open(
            self.DATA_FILE,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    def _validate(self):

        required = [

            "sku",

            "brand_name",

            "generic_name",

            "manufacturer",

            "category",

            "strength",

            "dosage_form",

            "package_size",

            "price",

        ]

        skus = set()

        for profile in self._profiles:

            for field in required:

                if field not in profile:

                    raise ValueError(
                        f"Missing '{field}'"
                    )

            sku = profile["sku"]

            if sku in skus:

                raise ValueError(
                    f"Duplicate SKU: {sku}"
                )

            skus.add(sku)

    def _build_indexes(self):

        for profile in self._profiles:

            self._sku_index[
                profile["sku"]
            ] = profile

            self._brand_index[
                profile["brand_name"]
            ] = profile

            self._generic_index[
                profile["generic_name"]
            ].append(profile)

            self._manufacturer_index[
                profile["manufacturer"]
            ].append(profile)

            self._category_index[
                profile["category"]
            ].append(profile)

    def _copy(self, value):

        return deepcopy(value)

    @property
    def profiles(self):

        return self._copy(
            self._profiles
        )


    @property
    def sku_index(self):

        return self._copy(
            self._sku_index
        )


    @property
    def brand_index(self):

        return self._copy(
            self._brand_index
        )


    @property
    def generic_index(self):

        return self._copy(
            self._generic_index
        )


    @property
    def manufacturer_index(self):

        return self._copy(
            self._manufacturer_index
        )


    @property
    def category_index(self):

        return self._copy(
            self._category_index
        )
    
    def all(self):
        """
        Returns all brand profiles.
        """

        return self._copy(
            self._profiles
        )

    def count(self):
        """
        Returns total brand profiles.
        """

        return len(
            self._profiles
        )

    def exists(
        self,
        brand_name,
    ):
        """
        Returns whether a brand exists.
        """

        return (
            brand_name
            in self._brand_index
        )

    def get_by_brand(
        self,
        brand_name,
    ):
        """
        Returns one brand profile.
        """

        profile = self._brand_index.get(
            brand_name
        )

        if profile is None:
            return None

        return self._copy(profile)

    def get_by_sku(
        self,
        sku,
    ):
        """
        Returns profile by SKU.
        """

        profile = self._sku_index.get(
            sku
        )

        if profile is None:
            return None

        return self._copy(profile)

    def by_generic(
        self,
        generic_name,
    ):
        """
        Returns all profiles for a generic.
        """

        return self._copy(

            self._generic_index.get(
                generic_name,
                [],
            )

        )

    def by_category(
        self,
        category,
    ):
        """
        Returns all profiles for a category.
        """

        return self._copy(

            self._category_index.get(
                category,
                [],
            )

        )

    def by_manufacturer(
        self,
        manufacturer,
    ):
        """
        Returns all profiles for a manufacturer.
        """

        return self._copy(

            self._manufacturer_index.get(
                manufacturer,
                [],
            )

        )

    def brand_names(self):
        """
        Returns all brand names.
        """

        return sorted(

            self._brand_index.keys()

        )

    def generic_names(self):
        """
        Returns all generic names.
        """

        return sorted(

            self._generic_index.keys()

        )

    def manufacturers(self):
        """
        Returns manufacturers.
        """

        return sorted(

            self._manufacturer_index.keys()

        )

    def categories(self):
        """
        Returns categories.
        """

        return sorted(

            self._category_index.keys()

        )

    def _field(
        self,
        brand_name,
        field,
    ):
        """
        Returns a single field from a brand profile.

        Parameters
        ----------
        brand_name : str

        field : str

        Returns
        -------
        Any
        """

        profile = self.get_by_brand(
            brand_name
        )

        if profile is None:

            return None

        return self._copy(

            profile.get(field)

        )

    def get_sku(
        self,
        brand_name,
    ):
        """
        Returns SKU.
        """

        return self._field(
            brand_name,
            "sku",
        )

    def get_brand_name(
        self,
        brand_name,
    ):
        """
        Returns brand name.
        """

        return self._field(
            brand_name,
            "brand_name",
        )

    def get_generic(
        self,
        brand_name,
    ):
        """
        Returns generic medicine.
        """

        return self._field(
            brand_name,
            "generic_name",
        )

    def get_manufacturer(
        self,
        brand_name,
    ):
        """
        Returns manufacturer.
        """

        return self._field(
            brand_name,
            "manufacturer",
        )

    def get_category(
        self,
        brand_name,
    ):
        """
        Returns category.
        """

        return self._field(
            brand_name,
            "category",
        )

    def get_therapeutic_class(
        self,
        brand_name,
    ):
        """
        Returns therapeutic class.
        """

        return self._field(
            brand_name,
            "therapeutic_class",
        )

    def get_strength(
        self,
        brand_name,
    ):
        """
        Returns strength.
        """

        return self._field(
            brand_name,
            "strength",
        )

    def get_dosage_form(
        self,
        brand_name,
    ):
        """
        Returns dosage form.
        """

        return self._field(
            brand_name,
            "dosage_form",
        ) 

    def get_package_size(
        self,
        brand_name,
    ):
        """
        Returns package size.
        """

        return self._field(
            brand_name,
            "package_size",
        )  

    def get_price(
        self,
        brand_name,
    ):
        """
        Returns price.
        """

        return self._field(
            brand_name,
            "price",
        ) 

    def get_currency(
        self,
        brand_name,
    ):
        """
        Returns currency.
        """

        return self._field(
            brand_name,
            "currency",
        ) 

    def prescription_required(
        self,
        brand_name,
    ):
        """
        Returns prescription flag.
        """

        return self._field(
            brand_name,
            "prescription_required",
        )

    def get_status(
        self,
        brand_name,
    ):
        """
        Returns status.
        """

        return self._field(
            brand_name,
            "status",
        )     

    def get_indications(
        self,
        brand_name,
    ):
        """
        Returns indications.
        """

        return self._field(
            brand_name,
            "indications",
        )    

    def get_side_effects(
        self,
        brand_name,
    ):
        """
        Returns side effects.
        """

        return self._field(
            brand_name,
            "side_effects",
        ) 

    def get_contraindications(
        self,
        brand_name,
    ):
        """
        Returns contraindications.
        """

        return self._field(
            brand_name,
            "contraindications",
        )     

    def get_storage(
        self,
        brand_name,
    ):
        """
        Returns storage instructions.
        """

        return self._field(
            brand_name,
            "storage",
        )
    
    def category_counts(self):
        """
        Returns number of brands per category.
        """

        return {
            category: len(items)
            for category, items in self._category_index.items()
        }
    
    def manufacturer_counts(self):
        """
        Returns number of brands per manufacturer.
        """

        return {
            manufacturer: len(items)
            for manufacturer, items in self._manufacturer_index.items()
        }

    from collections import Counter

    def therapeutic_class_counts(self):
        """
        Count therapeutic classes.
        """

        counter = Counter()

        for profile in self._profiles:
            counter[
                profile["therapeutic_class"]
            ] += 1

        return dict(counter)

    def dosage_form_counts(self):

        counter = Counter()

        for profile in self._profiles:

            counter[
                profile["dosage_form"]
            ] += 1

        return dict(counter)

    def strength_counts(self):

        counter = Counter()

        for profile in self._profiles:

            counter[
                profile["strength"]
            ] += 1

        return dict(counter)

    def package_size_counts(self):

        counter = Counter()

        for profile in self._profiles:

            counter[
                profile["package_size"]
            ] += 1

        return dict(counter)

    def prescription_counts(self):
        """
        Counts prescription/non-prescription medicines.
        """

        counter = Counter()

        for profile in self._profiles:

            counter[
                profile["prescription_required"]
            ] += 1

        return dict(counter)

    def status_counts(self):

        counter = Counter()

        for profile in self._profiles:

            counter[
                profile["status"]
            ] += 1

        return dict(counter)

    def average_price(self):
        """
        Returns average price.
        """

        prices = [

            profile["price"]

            for profile in self._profiles

        ]

        return round(

            sum(prices) / len(prices),

            2,

        )
    
    def min_price(self):

        return min(

            profile["price"]

            for profile in self._profiles

        )

    def max_price(self):

        return max(

            profile["price"]

            for profile in self._profiles

        )
    
    def summary(self):
        """
        Repository summary.
        """

        return {

            "profiles": self.count(),

            "brands": len(
                self._brand_index
            ),

            "manufacturers": len(
                self._manufacturer_index
            ),

            "categories": len(
                self._category_index
            ),

            "average_price": self.average_price(),

            "min_price": self.min_price(),

            "max_price": self.max_price(),

        }
    


