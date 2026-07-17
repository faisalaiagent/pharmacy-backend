"""
Production SKU Generator
------------------------

Generates unique pharmacy SKUs.

Example:

GET-PAR-500-TAB-000001
SEA-OME-020-CAP-000187
ABB-AMX-625-TAB-000942
"""

from __future__ import annotations

import random

from products.models import Product


class SKUGenerator:
    """
    Enterprise SKU Generator.
    """

    DOSAGE_CODES = {
        "Tablet": "TAB",
        "Capsule": "CAP",
        "Injection": "INJ",
        "Syrup": "SYP",
        "Suspension": "SUS",
        "Drops": "DRP",
        "Cream": "CRM",
        "Ointment": "ONT",
        "Gel": "GEL",
        "Spray": "SPY",
        "Inhaler": "INH",
        "Nebules": "NEB",
        "Eye Drops": "EYE",
        "Nasal Spray": "NAS",
        "Powder": "PWD",
        "Softgel": "SFG",
        "Patch": "PAT",
        "Solution": "SOL",
        "Lotion": "LOT",
        "Mouthwash": "MTH",
    }

    @staticmethod
    def manufacturer_prefix(name: str) -> str:
        """
        Get manufacturer prefix.

        Examples:
            Getz Pharma -> GET
            Sami Pharmaceuticals -> SAM
            Martin Dow -> MAR
        """

        if not name:
            return "GEN"

        words = str(name).strip().split()

        if not words:
            return "GEN"

        return words[0][:3].upper()

    @staticmethod
    def generic_prefix(generic_name: str) -> str:
        """
        Examples:
            Paracetamol -> PAR
            Amoxicillin -> AMO
        """

        if not generic_name:
            return "MED"

        cleaned = (
            str(generic_name)
            .replace("/", "")
            .replace("-", "")
            .replace(",", "")
            .replace("(", "")
            .replace(")", "")
            .strip()
        )

        if not cleaned:
            return "MED"

        return cleaned[:3].upper()

    @staticmethod
    def strength_code(strength: str) -> str:
        """
        Examples:

            500 mg -> 500
            1 g -> 1000
            0.5 % -> 05
            100 IU/ml -> 100
        """

        if not strength:
            return "000"

        digits = "".join(ch for ch in str(strength) if ch.isdigit())

        if digits:
            return digits[:4]

        return "000"

    @classmethod
    def dosage_code(cls, dosage_form):
        """
        Return a 3-letter dosage code.

        Handles None, empty strings and unknown dosage forms safely.
        """

        if not dosage_form:
            return "UNK"

        dosage_form = str(dosage_form).strip()

        if not dosage_form:
            return "UNK"

        mapping = {
            "Tablet": "TAB",
            "Capsule": "CAP",
            "Syrup": "SYP",
            "Injection": "INJ",
            "Cream": "CRM",
            "Gel": "GEL",
            "Drops": "DRP",
            "Suspension": "SUS",
            "Ointment": "ONT",
            "Powder": "PWD",
            "Spray": "SPY",
            "Inhaler": "INH",
            "Nebules": "NEB",
            "Eye Drops": "EYE",
            "Nasal Spray": "NAS",
            "Softgel": "SFG",
            "Patch": "PAT",
            "Solution": "SOL",
            "Lotion": "LOT",
            "Mouthwash": "MTH",
        }

        return mapping.get(
            dosage_form,
            dosage_form[:3].upper(),
        )

    @staticmethod
    def sequence():
        """
        Generates:

        000001
        000002
        ...
        """

        while True:

            seq = random.randint(1, 999999)

            yield f"{seq:06d}"

    @classmethod
    def generate(
        cls,
        manufacturer_name: str,
        generic_name: str,
        strength: str,
        dosage_form: str,
    ) -> str:
        """
        Build SKU.

        Example:

        GET-PAR-500-TAB-000123
        """

        manufacturer = cls.manufacturer_prefix(
            manufacturer_name
        )

        generic = cls.generic_prefix(
            generic_name
        )

        strength = cls.strength_code(
            strength
        )

        dosage = cls.dosage_code(
            dosage_form
        )

        generator = cls.sequence()

        while True:

            sku = (
                f"{manufacturer}-"
                f"{generic}-"
                f"{strength}-"
                f"{dosage}-"
                f"{next(generator)}"
            )

            if not Product.objects.filter(
                sku=sku
            ).exists():

                return sku


def generate_sku(
    manufacturer,
    generic_name,
    strength,
    dosage_form,
):
    """
    Shortcut helper.
    """

    manufacturer_name = ""

    if manufacturer:

        manufacturer_name = getattr(
            manufacturer,
            "name",
            ""
        )

    return SKUGenerator.generate(
        manufacturer_name=manufacturer_name,
        generic_name=generic_name,
        strength=strength,
        dosage_form=dosage_form,
    )