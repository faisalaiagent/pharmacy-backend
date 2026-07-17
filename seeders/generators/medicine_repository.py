"""
medicine_repository.py

Central repository responsible for loading all JSON datasets used by
the medicine generator framework.

This class isolates all file I/O from the rest of the generator so that
other modules simply request data from the repository.

Production Ready
----------------
✓ Automatic path resolution
✓ Safe JSON loading
✓ Empty-file handling
✓ Missing-file handling
✓ Cached datasets
✓ Strong typing
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MedicineRepository:
    """Loads and caches all pharmacy reference datasets."""

    DATA_DIR = Path(__file__).resolve().parent.parent / "data"

    def __init__(self):

        self._cache = {}

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------

    def _load_json(self, filename: str) -> Any:
        """
        Safely load a JSON file.

        Returns:
            list | dict

        Never raises JSON errors.
        Missing or empty files simply return [].
        """

        if filename in self._cache:
            return self._cache[filename]

        file_path = self.DATA_DIR / filename

        if not file_path.exists():
            print(f"[Repository] Missing: {filename}")
            self._cache[filename] = []
            return []

        if file_path.stat().st_size == 0:
            raise ValueError(
                f"{filename} is empty. Run the dataset generators first."
            )

        try:

            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError:

            print(f"[Repository] Invalid JSON: {filename}")
            data = []

        self._cache[filename] = data

        return data

    # ---------------------------------------------------------
    # Dataset getters
    # ---------------------------------------------------------

    def categories(self):

        return self._load_json("categories.json")

    def manufacturers(self):

        return self._load_json("manufacturers.json")
    
    def generic_names(self):
        """
        Returns the master generic medicine dataset.
        """

        return self._load_json("generic_names.json")

    def brands(self):

        return self._load_json("brands.json")

    def therapeutic_classes(self):

        return self._load_json("therapeutic_classes.json")

    def strengths(self):

        return self._load_json("strengths.json")

    def dosage_forms(self):

        return self._load_json("dosage_forms.json")

    def package_sizes(self):

        return self._load_json("package_sizes.json")

    def indications(self):

        return self._load_json("indications.json")

    def side_effects(self):

        return self._load_json("side_effects.json")

    def contraindications(self):

        return self._load_json("contraindications.json")

    def storage(self):

        return self._load_json("storage.json")

    def medicine_dictionary(self):

        return self._load_json("medicine_dictionary.json")

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def clear_cache(self):
        """Force reload on next access."""
        self._cache.clear()

    def dataset_summary(self):
        """
        Returns a quick summary of loaded datasets.
        """

        return {

            "categories": len(self.categories()),

            "manufacturers": len(self.manufacturers()),

            "generic_names": len(self.generic_names()),

            "brands": len(self.brands()),

            "therapeutic_classes": len(
                self.therapeutic_classes()
            ),

            "strengths": len(self.strengths()),

            "dosage_forms": len(self.dosage_forms()),

            "package_sizes": len(
                self.package_sizes()
            ),

            "indications": len(
                self.indications()
            ),

            "side_effects": len(
                self.side_effects()
            ),

            "contraindications": len(
                self.contraindications()
            ),

            "storage": len(self.storage()),

            "medicine_dictionary": len(
                self.medicine_dictionary()
            ),
        }

    def print_summary(self):
        """
        Pretty-print dataset statistics.
        """

        print("\n" + "=" * 60)
        print("Medicine Repository")
        print("=" * 60)

        summary = self.dataset_summary()

        for name, count in summary.items():

            print(f"{name:<25} {count:>6}")

        print("=" * 60)