"""
seeders/generators/brand_generator.py

Production Brand Generator

Creates realistic pharmaceutical brands.

Output:
    seeders/data/brands.json
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from .base_generator import BaseGenerator


DATA_DIR = Path(__file__).resolve().parent.parent / "data"

MANUFACTURERS_FILE = DATA_DIR / "manufacturers.json"
GENERIC_FILE = DATA_DIR / "generic_names.json"


PREFIXES = [
    "A",
    "Ace",
    "Neo",
    "Bio",
    "Cef",
    "Am",
    "Pro",
    "Ultra",
    "Max",
    "Med",
    "Uni",
    "Pan",
    "Tri",
    "Zen",
    "Nova",
    "Vita",
    "Safe",
    "Sure",
]

SUFFIXES = [
    "",
    "ex",
    "ix",
    "on",
    "in",
    "ol",
    "id",
    "ox",
    "max",
    "fort",
    "plus",
    "care",
    "vita",
]


class BrandGenerator(BaseGenerator):
    """
    Generates pharmaceutical brands.
    """

    OUTPUT_FILE = "brands.json"

    def __init__(self, seed: int = 42):

        super().__init__()

        random.seed(seed)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def load_json(self, path: Path):

        if not path.exists():
            return []

        if path.stat().st_size == 0:
            return []

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # Brand Name Builder
    # ---------------------------------------------------------

    def build_brand_name(self, generic: str):

        generic = generic.lower()

        cleaned = (
            generic.replace("/", "")
            .replace("-", "")
            .replace(",", "")
            .replace("(", "")
            .replace(")", "")
            .strip()
        )

        root = cleaned[:4].capitalize()

        prefix = random.choice(PREFIXES)

        suffix = random.choice(SUFFIXES)

        return f"{prefix}{root}{suffix}"

    # ---------------------------------------------------------
    # Main Generator
    # ---------------------------------------------------------

    def generate(self):

        manufacturers = self.load_json(
            MANUFACTURERS_FILE
        )

        generic_names  = self.load_json(
            GENERIC_FILE
        )

        if not manufacturers:
            raise ValueError(
                "manufacturers.json is empty."
            )

        if not generic_names :
            raise ValueError(
                "generic_names.json is empty."
            )

        results = []

        seen = set()

        for item in generic_names:

            generic = item.get(
                "generic_name"
            )

            if not generic:
                continue

            manufacturer = random.choice(
                manufacturers
            )

            brand_name = self.build_brand_name(
                generic
            )

            key = (
                brand_name,
                generic,
            )

            if key in seen:
                continue

            seen.add(key)

            results.append(
                {
                    "name": brand_name,
                    "generic_name": generic,
                    "manufacturer": manufacturer.get(
                        "name",
                        "",
                    ),
                    "country": "Pakistan",
                    "is_active": True,
                }
            )

        results.sort(
            key=lambda x: x["name"]
        )

        print(
            f"Generated {len(results)} brands."
        )

        return results


def generate_brands():
    """
    Helper function.

    Generates and exports brands.json.
    """

    return BrandGenerator().export()


if __name__ == "__main__":

    BrandGenerator().export()