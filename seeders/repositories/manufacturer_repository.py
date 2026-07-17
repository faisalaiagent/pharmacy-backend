from __future__ import annotations

import json
import random

from copy import deepcopy
from pathlib import Path
from collections import defaultdict


class ManufacturerRepository:
    """
    Repository for manufacturers.

    Loads manufacturers.json and provides
    fast lookup utilities.
    """

    DATA_FILE = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "manufacturers.json"
    )

    def __init__(self):

        self._manufacturers = self._load()

        self._validate()

        self._name_index = {}

        self._country_index = defaultdict(list)

        self._build_indexes()

    def _load(self):

        with open(
            self.DATA_FILE,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    def _validate(self):

        names = set()

        required = [

            "name",

            "country",

        ]

        for manufacturer in self._manufacturers:

            for field in required:

                if field not in manufacturer:

                    raise ValueError(
                        f"Missing '{field}'"
                    )

            name = manufacturer["name"]

            if name in names:

                raise ValueError(
                    f"Duplicate manufacturer: {name}"
                )

            names.add(name)

    def _build_indexes(self):

        for manufacturer in self._manufacturers:

            self._name_index[
                manufacturer["name"]
            ] = manufacturer

            self._country_index[
                manufacturer["country"]
            ].append(manufacturer)

    def _copy(self, value):

        return deepcopy(value)

    @property
    def manufacturers(self):

        return self._copy(
            self._manufacturers
        )


    @property
    def name_index(self):

        return self._copy(
            self._name_index
        )


    @property
    def country_index(self):

        return self._copy(
            self._country_index
        )        
    
    def all(self):

        return self._copy(
            self._manufacturers
        )


    def count(self):

        return len(
            self._manufacturers
        )


    def exists(
        self,
        name,
    ):

        return (
            name
            in self._name_index
        )


    def get(
        self,
        name,
    ):

        manufacturer = self._name_index.get(
            name
        )

        if manufacturer is None:
            return None

        return self._copy(
            manufacturer
        )


    def names(self):

        return sorted(
            self._name_index.keys()
        )


    def countries(self):

        return sorted(
            self._country_index.keys()
        )


    def by_country(
        self,
        country,
    ):

        return self._copy(
            self._country_index.get(
                country,
                [],
            )
        )
    
    def search(
        self,
        text,
    ):

        text = text.lower()

        return [

            self._copy(m)

            for m in self._manufacturers

            if text in m["name"].lower()

        ]


    def starts_with(
        self,
        prefix,
    ):

        prefix = prefix.lower()

        return [

            self._copy(m)

            for m in self._manufacturers

            if m["name"].lower().startswith(prefix)

        ]
    
    def random(self):

        return self._copy(
            random.choice(
                self._manufacturers
            )
        )


    def random_name(self):

        return random.choice(
            self.names()
        )


    def random_by_country(
        self,
        country,
    ):

        manufacturers = self.by_country(country)

        if not manufacturers:
            return None

        return random.choice(
            manufacturers
        )
    
    def country_counts(self):

        return {

            country: len(items)

            for country, items in sorted(
                self._country_index.items()
            )

        }


    def summary(self):

        return {

            "manufacturers": self.count(),

            "countries": len(
                self._country_index
            ),

        }
    
    def validate(self):

        self._validate()

        return True


    def validation_summary(self):

        return {

            "valid": self.validate(),

            "manufacturer_count": self.count(),

            "country_count": len(
                self._country_index
            ),

        }
    
    