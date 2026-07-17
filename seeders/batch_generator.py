"""
Production Batch Generator
--------------------------

Generates pharmaceutical batch information.

Example:

Batch Number : GET250704A
Lot Number   : LOT-3F9KX2
MFG Date     : 2026-07-04
Expiry Date  : 2029-06-30
"""

from __future__ import annotations

import random
import string
from datetime import date, timedelta


class BatchGenerator:
    """
    Enterprise Batch Generator.
    """

    @staticmethod
    def manufacturer_code(name: str) -> str:
        """
        Get manufacturer prefix.

        Getz Pharma -> GET
        Sami Pharmaceuticals -> SAM
        """

        if not name:
            return "GEN"

        return name.split()[0][:3].upper()

    @staticmethod
    def random_suffix(length: int = 1) -> str:
        """
        A-Z
        """

        return "".join(
            random.choices(
                string.ascii_uppercase,
                k=length,
            )
        )

    @classmethod
    def batch_number(
        cls,
        manufacturer_name: str,
    ) -> str:
        """
        Example

        GET260704A
        """

        today = date.today()

        return (
            f"{cls.manufacturer_code(manufacturer_name)}"
            f"{today.strftime('%y%m%d')}"
            f"{cls.random_suffix()}"
        )

    @staticmethod
    def lot_number() -> str:
        """
        Example

        LOT-9A4KX2
        """

        chars = string.ascii_uppercase + string.digits

        code = "".join(
            random.choices(
                chars,
                k=6,
            )
        )

        return f"LOT-{code}"

    @staticmethod
    def manufacturing_date(
        days_back: int = 180,
    ) -> date:
        """
        Manufacturing date between
        today and last 180 days.
        """

        return date.today() - timedelta(
            days=random.randint(0, days_back)
        )

    @staticmethod
    def expiry_date(
        manufacture_date: date,
        min_years: int = 2,
        max_years: int = 4,
    ) -> date:
        """
        Expiry between 2-4 years.
        """

        years = random.randint(
            min_years,
            max_years,
        )

        return manufacture_date + timedelta(
            days=365 * years
        )

    @staticmethod
    def shelf_life_months(
        manufacture_date: date,
        expiry_date: date,
    ) -> int:
        """
        Approximate shelf life.
        """

        return (
            (expiry_date - manufacture_date).days
            // 30
        )

    @classmethod
    def generate(
        cls,
        manufacturer_name: str,
    ) -> dict:
        """
        Complete batch information.
        """

        mfg = cls.manufacturing_date()

        exp = cls.expiry_date(mfg)

        return {

            "batch_number": cls.batch_number(
                manufacturer_name
            ),

            "lot_number": cls.lot_number(),

            "manufacturing_date": mfg,

            "expiry_date": exp,

            "shelf_life_months": cls.shelf_life_months(
                mfg,
                exp,
            ),
        }


def generate_batch(manufacturer):
    """
    Helper function.

    Returns batch dictionary.
    """

    manufacturer_name = ""

    if manufacturer:
        manufacturer_name = manufacturer.name

    return BatchGenerator.generate(
        manufacturer_name
    )