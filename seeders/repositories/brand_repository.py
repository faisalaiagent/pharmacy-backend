from __future__ import annotations

import json
import random
from collections import Counter
from copy import deepcopy
from pathlib import Path
from collections import defaultdict


class BrandRepository:
    """
    Repository for medicine brands.

    Loads brands.json and provides
    fast lookup utilities.
    """

    DATA_FILE = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "brands.json"
    )

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __init__(self):

        self._brands = self._load()

        self._validate()

        self._brand_index = {}

        self._generic_index = defaultdict(list)

        self._manufacturer_index = defaultdict(list)

    
        self._build_indexes()

    # ---------------------------------------------------------
    # Load JSON
    # ---------------------------------------------------------

    def _load(self):

        with open(
            self.DATA_FILE,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate(self):

        names = set()

        required = [
            "name",
            "generic_name",
            "manufacturer",
            "country",
        ]

        for brand in self._brands:

            for field in required:

                if field not in brand:

                    raise ValueError(
                        f"Missing '{field}'"
                    )

            brand_name = brand["name"]

            if brand_name in names:

                raise ValueError(
                    f"Duplicate brand: {brand_name}"
                )

            names.add(brand_name)

    # ---------------------------------------------------------
    # Build Indexes
    # ---------------------------------------------------------

    def _build_indexes(self):

        for brand in self._brands:

            self._brand_index[
                brand["name"]
            ] = brand

            self._generic_index[
                brand["generic_name"]
            ].append(brand)

            self._manufacturer_index[
                brand["manufacturer"]
            ].append(brand)

            

    # ---------------------------------------------------------
    # Copy Helper
    # ---------------------------------------------------------

    def _copy(
        self,
        value,
    ):

        return deepcopy(value)

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def brands(self):
        """
        Returns all brands.
        """

        return self._copy(
            self._brands
        )

    @property
    def brand_index(self):
        """
        Brand lookup index.
        """

        return self._copy(
            self._brand_index
        )

    @property
    def generic_index(self):
        """
        Generic medicine lookup index.
        """

        return self._copy(
            self._generic_index
        )

    @property
    def manufacturer_index(self):
        """
        Manufacturer lookup index.
        """

        return self._copy(
            self._manufacturer_index
        )

    # ---------------------------------------------------------
    # Lookup Methods
    # ---------------------------------------------------------

    def all(self):
        """
        Returns all brands.
        """

        return self._copy(
            self._brands
        )


    def count(self):
        """
        Returns total number of brands.
        """

        return len(
            self._brands
        )


    def exists(
        self,
        brand_name,
    ):
        """
        Checks whether a brand exists.
        """

        return (
            brand_name
            in self._brand_index
        )


    def get(
        self,
        brand_name,
    ):
        """
        Returns one brand.
        """

        brand = self._brand_index.get(
            brand_name
        )

        if brand is None:
            return None

        return self._copy(
            brand
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
        Returns all manufacturers.
        """

        return sorted(
            self._manufacturer_index.keys()
        )


    def countries(self):
        """
        Returns all countries.
        """

        return sorted(
            {
                brand["country"]
                for brand in self._brands
            }
        )


    def by_generic(
        self,
        generic_name,
    ):
        """
        Returns brands for a generic medicine.
        """

        return self._copy(
            self._generic_index.get(
                generic_name,
                [],
            )
        )


    def by_manufacturer(
        self,
        manufacturer,
    ):
        """
        Returns brands by manufacturer.
        """

        return self._copy(
            self._manufacturer_index.get(
                manufacturer,
                [],
            )
        )


    def by_country(
        self,
        country,
    ):
        """
        Returns brands manufactured in a country.
        """

        return [

            self._copy(brand)

            for brand in self._brands

            if brand["country"] == country

        ]
    
    def search(self, keyword):
        """
        Search brands by brand name,
        generic name, or manufacturer.
        """

        keyword = keyword.lower()

        results = []

        for brand in self._brands:

            if (
                keyword in brand["name"].lower()
                or keyword in brand["generic_name"].lower()
                or keyword in brand["manufacturer"].lower()
            ):
                results.append(
                    self._copy(brand)
                )

        return results
    
    def search_brand(self, keyword):
        """
        Search only brand names.
        """

        keyword = keyword.lower()

        return [

            self._copy(brand)

            for brand in self._brands

            if keyword in brand["name"].lower()

        ]
    
    def search_generic(self, keyword):
        """
        Search generic medicines.
        """

        keyword = keyword.lower()

        return [

            self._copy(brand)

            for brand in self._brands

            if keyword in brand["generic_name"].lower()

        ]
    
    def search_manufacturer(self, keyword):
        """
        Search manufacturers.
        """

        keyword = keyword.lower()

        return [

            self._copy(brand)

            for brand in self._brands

            if keyword in brand["manufacturer"].lower()

        ]
    
    def random(self):
        """
        Returns one random brand.
        """

        return self._copy(
            random.choice(
                self._brands
            )
        )
    
    def random_brand_name(self):
        """
        Returns random brand name.
        """

        return self.random()["name"]
    
    def random_generic(self):
        """
        Returns random generic.
        """

        return self.random()["generic_name"]

    def random_manufacturer(self):
        """
        Returns random manufacturer.
        """

        return self.random()["manufacturer"]
    
    def validate(self):
        """
        Validate repository.
        """

        assert self.count() > 0

        for brand in self._brands:

            assert brand["name"]

            assert brand["generic_name"]

            assert brand["manufacturer"]

        return True
    
    def validation_summary(self):
        """
        Validation summary.
        """

        return {

            "valid": self.validate(),

            "brand_count": self.count(),

            "manufacturer_count": len(
                self.manufacturers()
            ),

            "country_count": len(
                self.countries()
            ),

        }
    
    def manufacturer_counts(self):
        """
        Count brands per manufacturer.
        """

        counter = Counter()

        for brand in self._brands:

            counter[
                brand["manufacturer"]
            ] += 1

        return dict(counter)
    
    def country_counts(self):
        """
        Count brands by country.
        """

        counter = Counter()

        for brand in self._brands:

            counter[
                brand["country"]
            ] += 1

        return dict(counter)
    
    def generic_counts(self):
        """
        Count brands per generic.
        """

        counter = Counter()

        for brand in self._brands:

            counter[
                brand["generic_name"]
            ] += 1

        return dict(counter)
    
    def summary(self):
        """
        Repository summary.
        """

        return {

            "brands": self.count(),

            "manufacturers": len(
                self.manufacturers()
            ),

            "countries": len(
                self.countries()
            ),

            "generics": len(
                self.generic_names()
            ),

        }
    
    