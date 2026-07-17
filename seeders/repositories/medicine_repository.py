from __future__ import annotations

import json
import random

from copy import deepcopy
from pathlib import Path
from collections import defaultdict

class MedicineRepository:
    """
    Repository for generic medicines.

    Loads generic_names.json and provides
    fast lookup utilities.
    """

    DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "generic_names.json"
)
    
    def __init__(self):

        self._medicines = self._load()

        self._validate()

        self._generic_index = {}

        self._category_index = defaultdict(list)

        self._therapeutic_index = defaultdict(list)

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

            "generic_name",

            "category",

        ]

        for medicine in self._medicines:

            for field in required:

                if field not in medicine:

                    raise ValueError(

                        f"Missing '{field}'"

                    )

            name = medicine["generic_name"]

            if name in names:

                raise ValueError(

                    f"Duplicate generic: {name}"

                )

            names.add(name)

    def _build_indexes(self):

        for medicine in self._medicines:

            self._generic_index[
                medicine["generic_name"]
            ] = medicine

            self._category_index[
                medicine["category"]
            ].append(medicine)

            therapeutic = medicine.get(
                "therapeutic_class"
            )

            if therapeutic:

                self._therapeutic_index[
                    therapeutic
                ].append(medicine)

    def _copy(self, value):

        return deepcopy(value)

    @property
    def medicines(self):

        return self._copy(
            self._medicines
        )


    @property
    def generic_index(self):

        return self._copy(
            self._generic_index
        )


    @property
    def category_index(self):

        return self._copy(
            self._category_index
        )


    @property
    def therapeutic_index(self):

        return self._copy(
            self._therapeutic_index
        )                    

        # ---------------------------------------------------------
    # Lookup Methods
    # ---------------------------------------------------------

    def all(self):
        """
        Returns all medicines.
        """
        return self._copy(self._medicines)


    def count(self):
        """
        Returns total medicines.
        """
        return len(self._medicines)


    def exists(
        self,
        generic_name,
    ):
        """
        Returns True if generic exists.
        """
        return generic_name in self._generic_index


    def get(
        self,
        generic_name,
    ):
        """
        Returns one medicine.
        """
        medicine = self._generic_index.get(
            generic_name
        )

        if medicine is None:
            return None

        return self._copy(medicine)


    def generic_names(self):
        """
        Returns sorted generic names.
        """
        return sorted(
            self._generic_index.keys()
        )


    def categories(self):
        """
        Returns sorted categories.
        """
        return sorted(
            self._category_index.keys()
        )


    def by_category(
        self,
        category,
    ):
        """
        Returns medicines in category.
        """
        return self._copy(
            self._category_index.get(
                category,
                [],
            )
        )    
        random()

        random_generic()

        find()

        search()

        starts_with()

        ends_with()

        contains()

        random_by_category()

        summary()

        category_counts()

        alphabet_counts()

        validate()

        validation_summary()

        to_dict()

        to_json()

        to_dataframe()

        