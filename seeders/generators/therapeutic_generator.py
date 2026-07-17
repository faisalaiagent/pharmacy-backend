"""
seeders/generators/therapeutic_generator.py

Therapeutic Class Generator

Generates the master list of therapeutic classes used
throughout the AI Pharmacy project.

The JSON export is handled automatically by BaseGenerator.
"""

from __future__ import annotations

from .base_generator import BaseGenerator


class TherapeuticGenerator(BaseGenerator):
    """
    Generates therapeutic class reference data.
    """

    OUTPUT_FILE = "therapeutic_classes.json"

    def generate(self):

        therapeutic_classes = [

            {
                "name": "Analgesic",
                "category": "Pain Relief",
            },
            {
                "name": "NSAID",
                "category": "Pain Relief",
            },
            {
                "name": "Opioid Analgesic",
                "category": "Pain Relief",
            },

            {
                "name": "Penicillin Antibiotic",
                "category": "Antibiotics",
            },
            {
                "name": "Cephalosporin",
                "category": "Antibiotics",
            },
            {
                "name": "Macrolide",
                "category": "Antibiotics",
            },
            {
                "name": "Fluoroquinolone",
                "category": "Antibiotics",
            },

            {
                "name": "Biguanide",
                "category": "Diabetes",
            },
            {
                "name": "Sulfonylurea",
                "category": "Diabetes",
            },
            {
                "name": "DPP-4 Inhibitor",
                "category": "Diabetes",
            },
            {
                "name": "SGLT2 Inhibitor",
                "category": "Diabetes",
            },

            {
                "name": "ACE Inhibitor",
                "category": "Heart Care",
            },
            {
                "name": "ARB",
                "category": "Heart Care",
            },
            {
                "name": "Beta Blocker",
                "category": "Heart Care",
            },
            {
                "name": "Calcium Channel Blocker",
                "category": "Heart Care",
            },
            {
                "name": "Statin",
                "category": "Heart Care",
            },

            {
                "name": "Bronchodilator",
                "category": "Respiratory",
            },
            {
                "name": "Antihistamine",
                "category": "Respiratory",
            },
            {
                "name": "Corticosteroid",
                "category": "Respiratory",
            },

            {
                "name": "Proton Pump Inhibitor",
                "category": "Gastrointestinal",
            },
            {
                "name": "H2 Blocker",
                "category": "Gastrointestinal",
            },
            {
                "name": "Antacid",
                "category": "Gastrointestinal",
            },

            {
                "name": "Antifungal",
                "category": "Skin Care",
            },
            {
                "name": "Topical Steroid",
                "category": "Skin Care",
            },

            {
                "name": "Ophthalmic Antibiotic",
                "category": "Eye Care",
            },

            {
                "name": "ENT Antibiotic",
                "category": "ENT",
            },

            {
                "name": "Antiepileptic",
                "category": "Neurology",
            },

            {
                "name": "Antidepressant",
                "category": "Neurology",
            },

            {
                "name": "Urinary Antispasmodic",
                "category": "Urology",
            },

            {
                "name": "Hormonal Therapy",
                "category": "Women's Health",
            },

            {
                "name": "Vitamin",
                "category": "Vitamins & Supplements",
            },

            {
                "name": "Mineral",
                "category": "Vitamins & Supplements",
            },

        ]

        return therapeutic_classes


def generate_therapeutic_classes():
    """
    Convenience helper.
    """

    return TherapeuticGenerator().export()


if __name__ == "__main__":
    generate_therapeutic_classes()