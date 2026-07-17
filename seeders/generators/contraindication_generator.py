"""
seeders/generators/contraindication_generator.py

Generates contraindication reference dataset.

Output:
    seeders/data/contraindications.json
"""

from __future__ import annotations

from .base_generator import BaseGenerator


class ContraindicationGenerator(BaseGenerator):
    """
    Generates contraindication master data.
    """

    OUTPUT_FILE = "contraindications.json"

    DATA = [

        "Hypersensitivity to active ingredient",
        "Severe Liver Disease",
        "Severe Kidney Disease",
        "Pregnancy (when applicable)",
        "Breastfeeding (when applicable)",
        "History of Gastrointestinal Bleeding",
        "Active Peptic Ulcer",
        "Uncontrolled Hypertension",
        "Heart Block",
        "Severe Heart Failure",
        "Asthma induced by NSAIDs",
        "Glaucoma",
        "Myasthenia Gravis",
        "Severe Respiratory Depression",
        "Children under 2 years",
        "History of Seizures",
        "Porphyria",
        "Alcohol Dependence",
        "QT Prolongation",
        "Concurrent MAOI Therapy",

    ]

    def __init__(self):

        super().__init__()

    def generate(self):
        """
        Return contraindication dataset.

        BaseGenerator.export() automatically writes
        the JSON file.
        """

        return self.DATA


def generate_contraindications():
    """
    Convenience helper.
    """

    return ContraindicationGenerator().export()


if __name__ == "__main__":

    generate_contraindications()