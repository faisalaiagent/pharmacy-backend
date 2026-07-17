"""
seeders/generators/strength_generator.py

Generates pharmaceutical strength master data.
"""

from __future__ import annotations

from .base_generator import BaseGenerator


class StrengthGenerator(BaseGenerator):
    """
    Generates medicine strengths.
    """

    OUTPUT_FILE = "strengths.json"

    DATA = [

        "5mg",
        "10mg",
        "20mg",
        "25mg",
        "40mg",
        "50mg",
        "75mg",
        "100mg",
        "125mg",
        "250mg",
        "500mg",
        "650mg",
        "1000mg",

        "5ml",
        "10ml",
        "30ml",
        "60ml",
        "100ml",

        "250mg/5ml",
        "500mg/5ml",

        "0.5%",
        "1%",
        "2%",

        "5mcg",
        "10mcg",

    ]

    def generate(self):
        """
        Returns the strength dataset.
        """

        return self.DATA


def generate_strengths():
    """
    Convenience helper.
    """

    return StrengthGenerator().export()


if __name__ == "__main__":

    generate_strengths()