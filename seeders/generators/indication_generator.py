"""
seeders/generators/indication_generator.py

Generates indication reference dataset.

Output:
    seeders/data/indications.json
"""

from __future__ import annotations

from .base_generator import BaseGenerator


class IndicationGenerator(BaseGenerator):
    """
    Generates indication master data.
    """

    OUTPUT_FILE = "indications.json"

    DATA = [

        # Pain Relief
        "Headache",
        "Migraine",
        "Fever",
        "Body Pain",
        "Muscle Pain",
        "Joint Pain",
        "Back Pain",
        "Dental Pain",

        # Antibiotics
        "Bacterial Infection",
        "Respiratory Infection",
        "Urinary Tract Infection",
        "Skin Infection",
        "Ear Infection",
        "Eye Infection",
        "Typhoid Fever",

        # Diabetes
        "Type 2 Diabetes",
        "Type 1 Diabetes",
        "Blood Sugar Control",

        # Heart
        "Hypertension",
        "High Cholesterol",
        "Heart Failure",
        "Angina",
        "Arrhythmia",

        # Respiratory
        "Asthma",
        "COPD",
        "Allergic Rhinitis",
        "Seasonal Allergy",
        "Dry Cough",
        "Productive Cough",

        # Gastrointestinal
        "Acidity",
        "GERD",
        "Peptic Ulcer",
        "Constipation",
        "Diarrhea",
        "Nausea",
        "Vomiting",

        # Skin
        "Fungal Infection",
        "Eczema",
        "Dermatitis",
        "Acne",
        "Psoriasis",

        # Eye
        "Conjunctivitis",
        "Dry Eyes",
        "Eye Allergy",

        # ENT
        "Sinusitis",
        "Sore Throat",
        "Nasal Congestion",

        # Women's Health
        "Pregnancy Supplements",
        "Iron Deficiency",
        "Menstrual Pain",

        # Pediatrics
        "Child Fever",
        "Pediatric Infection",

        # Neurology
        "Epilepsy",
        "Neuropathic Pain",
        "Depression",
        "Anxiety",

        # Urology
        "Benign Prostatic Hyperplasia",
        "Overactive Bladder",

        # Oncology
        "Chemotherapy Support",
        "Cancer Pain",

        # Vitamins
        "Vitamin Deficiency",
        "Calcium Deficiency",
        "Immune Support",
        "General Weakness",

    ]

    def __init__(self):

        super().__init__()

    def generate(self):
        """
        Return indication dataset.

        BaseGenerator.export() automatically writes the JSON file.
        """

        return self.DATA


def generate_indications():
    """
    Helper function.
    """

    return IndicationGenerator().export()


if __name__ == "__main__":

    generate_indications()