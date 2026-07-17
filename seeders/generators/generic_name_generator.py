"""
seeders/generators/generic_name_generator.py

Production Generic Medicine Generator

Generates the master list of generic medicines used by the
entire pharmacy seeding pipeline.

Output
------
seeders/data/generic_names.json

This dataset is intentionally independent of brands.

Flow

generic_names.json
        ↓
brand_generator.py
        ↓
brands.json
        ↓
medicine_builder.py
"""

from __future__ import annotations

from .base_generator import BaseGenerator


class GenericNameGenerator(BaseGenerator):
    """
    Generates the master generic medicine dataset.
    """

    OUTPUT_FILE = "generic_names.json"

    DATA = [

        # =====================================================
        # Pain Relief / NSAIDs
        # =====================================================

        {
            "generic_name": "Paracetamol",
            "category": "Pain Relief",
        },
        {
            "generic_name": "Ibuprofen",
            "category": "Pain Relief",
        },
        {
            "generic_name": "Diclofenac",
            "category": "Pain Relief",
        },
        {
            "generic_name": "Naproxen",
            "category": "Pain Relief",
        },
        {
            "generic_name": "Ketorolac",
            "category": "Pain Relief",
        },

        # =====================================================
        # Antibiotics
        # =====================================================

        {
            "generic_name": "Amoxicillin",
            "category": "Antibiotics",
        },
        {
            "generic_name": "Co-Amoxiclav",
            "category": "Antibiotics",
        },
        {
            "generic_name": "Azithromycin",
            "category": "Antibiotics",
        },
        {
            "generic_name": "Clarithromycin",
            "category": "Antibiotics",
        },
        {
            "generic_name": "Cefixime",
            "category": "Antibiotics",
        },
        {
            "generic_name": "Ceftriaxone",
            "category": "Antibiotics",
        },
        {
            "generic_name": "Cefuroxime",
            "category": "Antibiotics",
        },
        {
            "generic_name": "Ciprofloxacin",
            "category": "Antibiotics",
        },
        {
            "generic_name": "Levofloxacin",
            "category": "Antibiotics",
        },
        {
            "generic_name": "Moxifloxacin",
            "category": "Antibiotics",
        },

        # =====================================================
        # Diabetes
        # =====================================================

        {
            "generic_name": "Metformin",
            "category": "Diabetes",
        },
        {
            "generic_name": "Glimepiride",
            "category": "Diabetes",
        },
        {
            "generic_name": "Gliclazide",
            "category": "Diabetes",
        },
        {
            "generic_name": "Sitagliptin",
            "category": "Diabetes",
        },
        {
            "generic_name": "Empagliflozin",
            "category": "Diabetes",
        },

        # =====================================================
        # Cardiovascular
        # =====================================================

        {
            "generic_name": "Amlodipine",
            "category": "Heart Care",
        },
        {
            "generic_name": "Losartan",
            "category": "Heart Care",
        },
        {
            "generic_name": "Valsartan",
            "category": "Heart Care",
        },
        {
            "generic_name": "Bisoprolol",
            "category": "Heart Care",
        },
        {
            "generic_name": "Metoprolol",
            "category": "Heart Care",
        },
        {
            "generic_name": "Rosuvastatin",
            "category": "Heart Care",
        },
        {
            "generic_name": "Atorvastatin",
            "category": "Heart Care",
        },
        {
            "generic_name": "Clopidogrel",
            "category": "Heart Care",
        },

        # =====================================================
        # Gastrointestinal
        # =====================================================

        {
            "generic_name": "Omeprazole",
            "category": "Gastrointestinal",
        },
        {
            "generic_name": "Esomeprazole",
            "category": "Gastrointestinal",
        },
        {
            "generic_name": "Pantoprazole",
            "category": "Gastrointestinal",
        },
        {
            "generic_name": "Rabeprazole",
            "category": "Gastrointestinal",
        },
        {
            "generic_name": "Domperidone",
            "category": "Gastrointestinal",
        },

        # =====================================================
        # Respiratory
        # =====================================================

        {
            "generic_name": "Salbutamol",
            "category": "Respiratory",
        },
        {
            "generic_name": "Montelukast",
            "category": "Respiratory",
        },
        {
            "generic_name": "Cetirizine",
            "category": "Respiratory",
        },
        {
            "generic_name": "Loratadine",
            "category": "Respiratory",
        },

        # =====================================================
        # Vitamins
        # =====================================================

        {
            "generic_name": "Vitamin C",
            "category": "Vitamins",
        },
        {
            "generic_name": "Vitamin D3",
            "category": "Vitamins",
        },
        {
            "generic_name": "Calcium Carbonate",
            "category": "Vitamins",
        },
        {
            "generic_name": "Ferrous Sulfate",
            "category": "Vitamins",
        },
        {
            "generic_name": "Folic Acid",
            "category": "Vitamins",
        },
    ]

    def generate(self):
        """
        Return the generic medicine dataset.
        BaseGenerator.export() will automatically
        validate and write it to generic_names.json.
        """

        return sorted(
            self.DATA,
            key=lambda item: item["generic_name"],
        )


def generate_generic_names():
    """
    Convenience helper.
    """

    return GenericNameGenerator().export()


if __name__ == "__main__":

    generate_generic_names()