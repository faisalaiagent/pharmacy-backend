"""
Production Regulatory Generator
-------------------------------

Generates realistic pharmaceutical regulatory information
for products marketed in Pakistan.

Example

Approval Number : DRAP-2026-483921
Registration ID : REG-PK-7A8F3Q91
Status          : Approved
Approval Date   : 2025-08-12
Renewal Date    : 2030-08-12
"""

from __future__ import annotations

import random
import string
from datetime import date, timedelta


class RegulatoryGenerator:
    """
    Generates realistic pharmaceutical regulatory data.
    """

    APPROVAL_STATUSES = (
        "Approved",
        "Approved",
        "Approved",
        "Approved",
        "Pending Renewal",
        "Provisionally Approved",
    )

    COUNTRY_CODES = {
        "Pakistan": "PK",
        "United Kingdom": "UK",
        "United States": "US",
        "Germany": "DE",
        "France": "FR",
        "Switzerland": "CH",
        "India": "IN",
        "China": "CN",
    }

    @staticmethod
    def approval_number() -> str:
        """
        Example

        DRAP-2026-483921
        """

        year = date.today().year

        serial = random.randint(
            100000,
            999999,
        )

        return f"DRAP-{year}-{serial}"

    @classmethod
    def registration_id(
        cls,
        country="Pakistan",
    ) -> str:
        """
        Example

        REG-PK-83KLM91Q
        """

        code = cls.COUNTRY_CODES.get(
            country,
            "PK",
        )

        chars = string.ascii_uppercase + string.digits

        random_code = "".join(
            random.choices(
                chars,
                k=8,
            )
        )

        return f"REG-{code}-{random_code}"

    @staticmethod
    def approval_date():
        """
        Random approval date
        during the last five years.
        """

        today = date.today()

        days_back = random.randint(
            180,
            365 * 5,
        )

        return today - timedelta(days=days_back)

    @staticmethod
    def renewal_date(
        approval_date,
    ):
        """
        Regulatory renewal after five years.
        """

        return approval_date + timedelta(
            days=365 * 5
        )

    @classmethod
    def approval_status(cls):

        return random.choice(
            cls.APPROVAL_STATUSES
        )

    @classmethod
    def generate(
        cls,
        country="Pakistan",
    ):

        approval = cls.approval_date()

        return {

            "regulatory_approval_number":
                cls.approval_number(),

            "registration_id":
                cls.registration_id(
                    country
                ),

            "approval_status":
                cls.approval_status(),

            "approval_date":
                approval,

            "renewal_date":
                cls.renewal_date(
                    approval
                ),
        }


def generate_regulatory(
    country="Pakistan",
):
    """
    Shortcut helper.
    """

    return RegulatoryGenerator.generate(
        country
    )