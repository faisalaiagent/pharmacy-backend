from __future__ import annotations

import json
import random
from copy import deepcopy
from pathlib import Path


class MedicineProfileRepository:
    """
    Repository for medicine compatibility profiles.

    Responsibilities
    ----------------
    • Load medicine_profiles.json
    • Validate dataset
    • Cache profiles
    • Build lookup indexes

    Does NOT generate data.
    """

    DATA_DIR = (
        Path(__file__).resolve().parent.parent
        / "data"
    )

    PROFILE_FILE = (
        DATA_DIR
        / "medicine_profiles.json"
    )

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __init__(self):

        self._profiles = self._load_profiles()

        self._validate_profiles()

        self._build_indexes()

    # ---------------------------------------------------------
    # Load JSON
    # ---------------------------------------------------------

    def _load_profiles(self):
        """
        Load medicine_profiles.json
        """

        if not self.PROFILE_FILE.exists():

            raise FileNotFoundError(
                f"{self.PROFILE_FILE.name} not found."
            )

        if self.PROFILE_FILE.stat().st_size == 0:

            raise ValueError(
                f"{self.PROFILE_FILE.name} is empty."
            )

        with open(
            self.PROFILE_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):

            raise ValueError(
                "medicine_profiles.json must contain a list."
            )

        return data

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate_profiles(self):
        """
        Validate loaded profiles.
        """

        seen = set()

        required_fields = [

            "generic_name",

            "category",

            "strengths",

            "dosage_forms",

            "package_sizes",

        ]

        for profile in self._profiles:

            generic = profile.get(
                "generic_name"
            )

            if not generic:

                raise ValueError(
                    "Profile missing generic_name."
                )

            if generic in seen:

                raise ValueError(
                    f"Duplicate profile: {generic}"
                )

            seen.add(generic)

            for field in required_fields:

                if field not in profile:

                    raise ValueError(
                        f"{generic} missing '{field}'"
                    )

    # ---------------------------------------------------------
    # Build Indexes
    # ---------------------------------------------------------

    def _build_indexes(self):
        """
        Build fast lookup dictionaries.
        """

        self._generic_index = {

            profile["generic_name"]: profile

            for profile in self._profiles

        }

        self._category_index = {}

        for profile in self._profiles:

            category = profile["category"]

            self._category_index.setdefault(
                category,
                [],
            ).append(profile)

    # ---------------------------------------------------------
    # Internal Helpers
    # ---------------------------------------------------------

    def _copy(
        self,
        value,
    ):
        """
        Return deep copy.
        """

        return deepcopy(value)

    # ---------------------------------------------------------
    # Basic Accessors
    # ---------------------------------------------------------

    @property
    def profiles(self):
        """
        Cached profiles.
        """

        return self._copy(
            self._profiles
        )

    @property
    def generic_index(self):
        """
        Generic lookup index.
        """

        return self._copy(
            self._generic_index
        )

    @property
    def category_index(self):
        """
        Category lookup index.
        """

        return self._copy(
            self._category_index
        )
    
    # ---------------------------------------------------------
    # Lookup Methods
    # ---------------------------------------------------------

    def all(self):
        """
        Returns all medicine profiles.

        Returns
        -------
        list[dict]
        """

        return self._copy(
            self._profiles
        )


    def count(self):
        """
        Returns total number of medicine profiles.

        Returns
        -------
        int
        """

        return len(
            self._profiles
        )


    def exists(
        self,
        generic_name,
    ):
        """
        Checks whether a generic medicine exists.

        Parameters
        ----------
        generic_name : str

        Returns
        -------
        bool
        """

        return (
            generic_name
            in self._generic_index
        )


    def get(
        self,
        generic_name,
    ):
        """
        Returns a medicine profile.

        Parameters
        ----------
        generic_name : str

        Returns
        -------
        dict | None
        """

        profile = self._generic_index.get(
            generic_name
        )

        if profile is None:

            return None

        return self._copy(
            profile
        )


    def generic_names(self):
        """
        Returns all generic medicine names.

        Returns
        -------
        list[str]
        """

        return sorted(
            self._generic_index.keys()
        )


    def categories(self):
        """
        Returns all available categories.

        Returns
        -------
        list[str]
        """

        return sorted(
            self._category_index.keys()
        )


    def by_category(
        self,
        category,
    ):
        """
        Returns all medicines belonging
        to one category.

        Parameters
        ----------
        category : str

        Returns
        -------
        list[dict]
        """

        medicines = self._category_index.get(
            category,
            [],
        )

        return self._copy(
            medicines
        )
    
    # ---------------------------------------------------------
    # Compatibility Accessors
    # ---------------------------------------------------------

    def get_therapeutic_class(
        self,
        generic_name,
    ):
        """
        Returns the primary therapeutic class.
        """

        profile = self.get(generic_name)

        if profile is None:
            return None

        return profile.get(
            "therapeutic_class"
        )


    def get_therapeutic_classes(
        self,
        generic_name,
    ):
        """
        Returns all compatible therapeutic classes.
        """

        profile = self.get(generic_name)

        if profile is None:
            return []

        return self._copy(
            profile.get(
                "therapeutic_classes",
                [],
            )
        )


    def get_strengths(
        self,
        generic_name,
    ):
        """
        Returns compatible strengths.
        """

        profile = self.get(generic_name)

        if profile is None:
            return []

        return self._copy(
            profile.get(
                "strengths",
                [],
            )
        )


    def get_dosage_forms(
        self,
        generic_name,
    ):
        """
        Returns compatible dosage forms.
        """

        profile = self.get(generic_name)

        if profile is None:
            return []

        return self._copy(
            profile.get(
                "dosage_forms",
                [],
            )
        )


    def get_package_sizes(
        self,
        generic_name,
    ):
        """
        Returns compatible package sizes.
        """

        profile = self.get(generic_name)

        if profile is None:
            return []

        return self._copy(
            profile.get(
                "package_sizes",
                [],
            )
        )


    def get_indications(
        self,
        generic_name,
    ):
        """
        Returns indications.
        """

        profile = self.get(generic_name)

        if profile is None:
            return []

        return self._copy(
            profile.get(
                "indications",
                [],
            )
        )


    def get_side_effects(
        self,
        generic_name,
    ):
        """
        Returns side effects.
        """

        profile = self.get(generic_name)

        if profile is None:
            return []

        return self._copy(
            profile.get(
                "side_effects",
                [],
            )
        )


    def get_contraindications(
        self,
        generic_name,
    ):
        """
        Returns contraindications.
        """

        profile = self.get(generic_name)

        if profile is None:
            return []

        return self._copy(
            profile.get(
                "contraindications",
                [],
            )
        )


    def get_storage(
        self,
        generic_name,
    ):
        """
        Returns storage instructions.
        """

        profile = self.get(generic_name)

        if profile is None:
            return []

        return self._copy(
            profile.get(
                "storage",
                [],
            )
        )


    def get_category(
        self,
        generic_name,
    ):
        """
        Returns medicine category.
        """

        profile = self.get(generic_name)

        if profile is None:
            return None

        return profile.get(
            "category"
        )

    # ---------------------------------------------------------
    # Random Selection Helpers
    # ---------------------------------------------------------

    import random


    def random_profile(self):
        """
        Returns a random medicine profile.

        Returns
        -------
        dict | None
        """

        if not self._profiles:
            return None

        return self._copy(
            random.choice(
                self._profiles
            )
        )


    def random_generic(self):
        """
        Returns a random generic medicine name.

        Returns
        -------
        str | None
        """

        if not self._profiles:
            return None

        return random.choice(
            self.generic_names()
        )


    def random_by_category(
        self,
        category,
    ):
        """
        Returns a random medicine from a category.
        """

        medicines = self.by_category(category)

        if not medicines:
            return None

        return self._copy(
            random.choice(
                medicines
            )
        )


    def random_strength(
        self,
        generic_name,
    ):
        """
        Returns one compatible strength.
        """

        strengths = self.get_strengths(
            generic_name
        )

        if not strengths:
            return None

        return random.choice(
            strengths
        )


    def random_dosage_form(
        self,
        generic_name,
    ):
        """
        Returns one compatible dosage form.
        """

        forms = self.get_dosage_forms(
            generic_name
        )

        if not forms:
            return None

        return random.choice(
            forms
        )


    def random_package_size(
        self,
        generic_name,
    ):
        """
        Returns one compatible package size.
        """

        packages = self.get_package_sizes(
            generic_name
        )

        if not packages:
            return None

        return random.choice(
            packages
        )        
    
    # ---------------------------------------------------------
    # Search Utilities
    # ---------------------------------------------------------

    def find_by_therapeutic_class(
        self,
        therapeutic_class,
    ):
        """
        Returns medicines matching a therapeutic class.
        """

        results = []

        for profile in self._profiles:

            if therapeutic_class in profile.get(
                "therapeutic_classes",
                [],
            ):

                results.append(
                    self._copy(profile)
                )

        return results


    def find_by_strength(
        self,
        strength,
    ):
        """
        Returns medicines supporting a strength.
        """

        results = []

        for profile in self._profiles:

            if strength in profile.get(
                "strengths",
                [],
            ):

                results.append(
                    self._copy(profile)
                )

        return results


    def find_by_dosage_form(
        self,
        dosage_form,
    ):
        """
        Returns medicines supporting a dosage form.
        """

        results = []

        for profile in self._profiles:

            if dosage_form in profile.get(
                "dosage_forms",
                [],
            ):

                results.append(
                    self._copy(profile)
                )

        return results


    def find_by_indication(
        self,
        indication,
    ):
        """
        Returns medicines matching an indication.
        """

        results = []

        for profile in self._profiles:

            if indication in profile.get(
                "indications",
                [],
            ):

                results.append(
                    self._copy(profile)
                )

        return results


    def search(
        self,
        keyword,
    ):
        """
        Performs a case-insensitive search by generic name,
        category, therapeutic class and indication.
        """

        keyword = keyword.lower()

        results = []

        for profile in self._profiles:

            if (
                keyword
                in profile["generic_name"].lower()
            ):
                results.append(
                    self._copy(profile)
                )
                continue

            if (
                keyword
                in profile["category"].lower()
            ):
                results.append(
                    self._copy(profile)
                )
                continue

            therapeutic_classes = [
                item.lower()
                for item in profile.get(
                    "therapeutic_classes",
                    [],
                )
            ]

            if keyword in therapeutic_classes:

                results.append(
                    self._copy(profile)
                )
                continue

            indications = [
                item.lower()
                for item in profile.get(
                    "indications",
                    [],
                )
            ]

            if keyword in indications:

                results.append(
                    self._copy(profile)
                )

        return results    
    
    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(self):
        """
        Validates the repository.

        Raises
        ------
        ValueError
            If invalid data is found.

        Returns
        -------
        bool
        """

        if not self._profiles:
            raise ValueError(
                "No medicine profiles loaded."
            )

        names = set()

        for profile in self._profiles:

            generic = profile["generic_name"]

            if generic in names:

                raise ValueError(
                    f"Duplicate generic medicine: {generic}"
                )

            names.add(generic)

            required = [

                "generic_name",
                "category",
                "therapeutic_class",
                "therapeutic_classes",
                "strengths",
                "dosage_forms",
                "package_sizes",
                "indications",
                "side_effects",
                "contraindications",
                "storage",

            ]

            for field in required:

                if field not in profile:

                    raise ValueError(
                        f"{generic}: Missing '{field}'."
                    )

            if not profile["strengths"]:

                raise ValueError(
                    f"{generic}: No strengths."
                )

            if not profile["dosage_forms"]:

                raise ValueError(
                    f"{generic}: No dosage forms."
                )

            if not profile["package_sizes"]:

                raise ValueError(
                    f"{generic}: No package sizes."
                )

        return True
    
    def validation_summary(self):
        """
        Returns validation information.
        """

        return {

            "valid": self.validate(),

            "medicine_count": self.count(),

            "category_count": len(
                self.categories()
            ),

        }
    
    def category_counts(self):
        """
        Returns medicine count per category.
        """

        counts = {}

        for category in self.categories():

            counts[category] = len(

                self.by_category(category)

            )

        return counts
    
    def category_counts(self):
        """
        Returns medicine count per category.
        """

        counts = {}

        for category in self.categories():

            counts[category] = len(

                self.by_category(category)

            )

        return counts
    
    def therapeutic_class_counts(self):

        counts = {}

        for profile in self._profiles:

            tc = profile["therapeutic_class"]

            counts[tc] = counts.get(tc, 0) + 1

        return counts
    
    def dosage_form_counts(self):

        counts = {}

        for profile in self._profiles:

            for form in profile["dosage_forms"]:

                counts[form] = counts.get(form, 0) + 1

        return counts
    
    def strength_counts(self):

        counts = {}

        for profile in self._profiles:

            for strength in profile["strengths"]:

                counts[strength] = counts.get(strength, 0) + 1

        return counts
    
    def package_size_counts(self):

        counts = {}

        for profile in self._profiles:

            for package in profile["package_sizes"]:

                counts[package] = counts.get(package, 0) + 1

        return counts
    
    def indication_counts(self):

        counts = {}

        for profile in self._profiles:

            for indication in profile["indications"]:

                counts[indication] = counts.get(indication, 0) + 1

        return counts
    
    def side_effect_counts(self):

        counts = {}

        for profile in self._profiles:

            for effect in profile["side_effects"]:

                counts[effect] = counts.get(effect, 0) + 1

        return counts
    
    def summary(self):
        """
        Returns repository statistics.
        """

        return {

            "medicine_profiles": self.count(),

            "categories": len(
                self.categories()
            ),

            "therapeutic_classes": len(
                self.therapeutic_class_counts()
            ),

            "dosage_forms": len(
                self.dosage_form_counts()
            ),

            "strengths": len(
                self.strength_counts()
            ),

            "package_sizes": len(
                self.package_size_counts()
            ),

            "indications": len(
                self.indication_counts()
            ),

        }
    
    