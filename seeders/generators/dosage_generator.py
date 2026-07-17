"""
seeders/generators/dosage_generator.py

Generates dosage form reference dataset.

Output:
    seeders/data/dosage_forms.json
"""

from __future__ import annotations

from .base_generator import BaseGenerator


class DosageGenerator(BaseGenerator):
    """
    Generates dosage form master data.
    """

    OUTPUT_FILE = "dosage_forms.json"

    DATA = [

        "Tablet",
        "Capsule",
        "Syrup",
        "Suspension",
        "Drops",
        "Injection",
        "Infusion",
        "Cream",
        "Ointment",
        "Gel",
        "Lotion",
        "Spray",
        "Nasal Spray",
        "Eye Drops",
        "Ear Drops",
        "Suppository",
        "Inhaler",
        "Respules",
        "Powder",
        "Oral Sachet",

    ]

    def __init__(self):

        super().__init__()

    def generate(self):
        """
        Return dosage forms.

        BaseGenerator.export() automatically writes the JSON file.
        """

        return self.DATA


def generate_dosage_forms():
    """
    Helper function.
    """

    return DosageGenerator().export()


if __name__ == "__main__":

    generate_dosage_forms()