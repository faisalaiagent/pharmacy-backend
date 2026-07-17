"""
seeders/generators/medicine_profile_generator.py

===============================================================
AI Pharmacy Medicine Profile Generator
===============================================================

Generates:

    seeders/data/medicine_profiles.json

Purpose
-------
Creates medically compatible profiles for every generic medicine.

Instead of randomly combining strengths, dosage forms and package
sizes, every generic medicine receives a validated compatibility
profile.

Pipeline

generic_names.json
        │
        ▼
medicine_profiles.json
        │
        ▼
MedicineBuilder
        │
        ▼
Product Seeder
        │
        ▼
Database

Author
------
AI Pharmacy Platform
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from .base_generator import BaseGenerator


class MedicineProfileGenerator(BaseGenerator):
    """
    Generates compatibility profiles for every generic medicine.
    """

    OUTPUT_FILE = "medicine_profiles.json"

    DATA_DIR = (
        Path(__file__).resolve().parent.parent
        / "data"
    )

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __init__(self):

        super().__init__()

        self.generic_file = (
            self.DATA_DIR
            / "generic_names.json"
        )

        self.therapeutic_file = (
            self.DATA_DIR
            / "therapeutic_classes.json"
        )

        self.strength_file = (
            self.DATA_DIR
            / "strengths.json"
        )

        self.dosage_file = (
            self.DATA_DIR
            / "dosage_forms.json"
        )

        self.package_file = (
            self.DATA_DIR
            / "package_sizes.json"
        )

        self.indication_file = (
            self.DATA_DIR
            / "indications.json"
        )

        self.side_effect_file = (
            self.DATA_DIR
            / "side_effects.json"
        )

        self.contra_file = (
            self.DATA_DIR
            / "contraindications.json"
        )

        self.storage_file = (
            self.DATA_DIR
            / "storage.json"
        )

        # ---------------------------------------------
        # Cached datasets
        # ---------------------------------------------

        self.generic_medicines = self.load_json(
            self.generic_file
        )

        self.therapeutic_classes = self.load_json(
            self.therapeutic_file
        )

        self.strengths = self.load_json(
            self.strength_file
        )

        self.dosage_forms = self.load_json(
            self.dosage_file
        )

        self.package_sizes = self.load_json(
            self.package_file
        )

        self.indications = self.load_json(
            self.indication_file
        )

        self.side_effects = self.load_json(
            self.side_effect_file
        )

        self.contraindications = self.load_json(
            self.contra_file
        )

        self.storage_rules = self.load_json(
            self.storage_file
        )

    # ---------------------------------------------------------
    # JSON Loader
    # ---------------------------------------------------------

    def load_json(
        self,
        file_path: Path,
    ) -> list[Any]:

        if not file_path.exists():

            raise FileNotFoundError(
                f"{file_path.name} not found."
            )

        if file_path.stat().st_size == 0:

            raise ValueError(
                f"{file_path.name} is empty."
            )

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    # ---------------------------------------------------------
    # Validators
    # ---------------------------------------------------------

    def ensure_list(
        self,
        value,
    ):

        if value is None:
            return []

        if isinstance(value, list):
            return value

        return [value]

    def require(
        self,
        value,
        message,
    ):

        if not value:
            raise ValueError(message)

        return value

    # ---------------------------------------------------------
    # Dataset Accessors
    # ---------------------------------------------------------

    def get_generic_medicines(self):

        return deepcopy(
            self.generic_medicines
        )

    def get_strengths(self) -> list[str]:

        return deepcopy(
            self.strengths
        )

    def get_dosage_forms(self):

        return deepcopy(
            self.dosage_forms
        )

    def get_package_sizes(self):

        return deepcopy(
            self.package_sizes
        )

    def get_indications(self):

        return deepcopy(
            self.indications
        )

    def get_side_effects(self):

        return deepcopy(
            self.side_effects
        )

    def get_contraindications(self):

        return deepcopy(
            self.contraindications
        )

    def get_storage_rules(self):

        return deepcopy(
            self.storage_rules
        )

    def get_therapeutic_classes(self):

        return deepcopy(
            self.therapeutic_classes
        )

    # ---------------------------------------------------------
    # Generic Helper
    # ---------------------------------------------------------

    def generic_names(self):

        return [
            medicine.get("generic_name")
            for medicine in self.generic_medicines
            if medicine.get("generic_name")
        ]

    def categories(self):

        return sorted(
            {
                medicine["category"]
                for medicine in self.generic_medicines
            }
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_dataset(self):

        self.generic_medicines = self.load_json(
            self.generic_file
        )

        self.require(
            self.generic_medicines,
            "generic_names.json is empty.",
        )

        self.require(
            self.therapeutic_classes,
            "therapeutic_classes.json is empty.",
        )

        self.require(
            self.strengths,
            "strengths.json is empty.",
        )

        self.require(
            self.dosage_forms,
            "dosage_forms.json is empty.",
        )

        self.require(
            self.package_sizes,
            "package_sizes.json is empty.",
        )

        self.require(
            self.indications,
            "indications.json is empty.",
        )

        self.require(
            self.side_effects,
            "side_effects.json is empty.",
        )

        self.require(
            self.contraindications,
            "contraindications.json is empty.",
        )

        self.require(
            self.storage_rules,
            "storage.json is empty.",
        )

        return True
    # ---------------------------------------------------------
    # Category Compatibility Rules
    # ---------------------------------------------------------

    def category_rules(self):
        """
        Default compatibility rules for each medicine category.
        Medicine-specific overrides will be applied later.
        """

        return {

            # -------------------------------------------------
            # Pain Relief
            # -------------------------------------------------

            "Pain Relief": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Analgesic",
                    "NSAID",
                    "Opioid Analgesic",

                ],

                # Available strengths
                "strengths": [

                    "250mg",
                    "500mg",
                    "650mg",
                    "1000mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Tablet",
                    "Capsule",
                    "Suspension",
                    "Syrup",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Strip of 10",
                    "Strip of 20",
                    "Bottle of 30",
                    "Bottle of 100",

                ],

                # Common indications
                "indications": [

                    "Headache",
                    "Migraine",
                    "Fever",
                    "Body Pain",
                    "Muscle Pain",
                    "Joint Pain",
                    "Back Pain",
                    "Dental Pain",

                ],

                # Common side effects
                "side_effects": [

                    "Nausea",
                    "Vomiting",
                    "Abdominal Pain",
                    "Dizziness",

                ],

                # Contraindications
                "contraindications": [

                    "Severe Liver Disease",
                    "History of Gastrointestinal Bleeding",

                ],

                # Storage instructions
                "storage": [

                    "Store below 30°C.",
                    "Keep out of reach of children.",

                ],

            },

            # -------------------------------------------------
            # Antibiotics
            # -------------------------------------------------

            "Antibiotics": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Penicillin Antibiotic",

                    "Cephalosporin",

                    "Macrolide",

                    "Fluoroquinolone",

                ],

                # Available strengths
                "strengths": [

                    "125mg",
                    "250mg",
                    "500mg",
                    "1000mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Tablet",
                    "Capsule",
                    "Suspension",
                    "Injection",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Strip of 10",
                    "60ml Bottle",
                    "100ml Bottle",
                    "Vial",

                ],

                # Common indications
                "indications": [

                    "Bacterial Infection",
                    "Respiratory Infection",
                    "Skin Infection",
                    "Ear Infection",
                    "Eye Infection",
                    "Urinary Tract Infection",

                ],

                # Common side effects
                "side_effects": [

                    "Diarrhea",
                    "Nausea",
                    "Vomiting",
                    "Skin Rash",

                ],

                # Contraindications
                "contraindications": [

                    "Hypersensitivity to active ingredient",

                ],

                # Storage instructions
                "storage": [

                    "Store below 30°C.",

                ],

            },

            # -------------------------------------------------
            # Diabetes
            # -------------------------------------------------

            "Diabetes": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Biguanide",

                    "Sulfonylurea",

                    "DPP-4 Inhibitor",

                    "SGLT2 Inhibitor",

                ],

                # Available strengths
                "strengths": [

                    "250mg",
                    "500mg",
                    "1000mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Tablet",
                    "Capsule",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Strip of 10",
                    "Strip of 20",
                    "Bottle of 30",
                    "Bottle of 60",

                ],

                # Common indications
                "indications": [

                    "Type 2 Diabetes",
                    "Blood Sugar Control",

                ],

                # Common side effects
                "side_effects": [

                    "Nausea",
                    "Diarrhea",
                    "Loss of Appetite",

                ],

                # Contraindications
                "contraindications": [

                    "Severe Kidney Disease",

                ],

                # Storage instructions
                "storage": [

                    "Store below 30°C.",
                    "Keep out of reach of children.",

                ],

            },

            # -------------------------------------------------
            # Heart Care
            # -------------------------------------------------

            "Heart Care": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "ACE Inhibitor",

                    "ARB",

                    "Beta Blocker",

                    "Calcium Channel Blocker",

                    "Statin",

                ],

                # Available strengths
                "strengths": [

                    "5mg",
                    "10mg",
                    "20mg",
                    "40mg",
                    "50mg",
                    "100mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Tablet",
                    "Capsule",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Strip of 10",
                    "Strip of 20",
                    "Bottle of 30",
                    "Bottle of 60",

                ],

                # Common indications
                "indications": [

                    "Hypertension",
                    "Heart Failure",
                    "High Cholesterol",
                    "Angina",
                    "Arrhythmia",

                ],

                # Common side effects
                "side_effects": [

                    "Dizziness",
                    "Hypotension",
                    "Fatigue",
                    "Headache",

                ],

                # Contraindications
                "contraindications": [

                    "Heart Block",
                    "Severe Heart Failure",
                    "Pregnancy (when applicable)",

                ],

                # Storage instructions
                "storage": [

                    "Store below 30°C.",
                    "Keep out of reach of children.",

                ],

            },

            # -------------------------------------------------
            # Gastrointestinal
            # -------------------------------------------------

            "Gastrointestinal": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Proton Pump Inhibitor",

                    "H2 Blocker",

                    "Antacid",

                ],

                # Available strengths
                "strengths": [

                    "20mg",
                    "40mg",
                    "250mg",
                    "500mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Tablet",
                    "Capsule",
                    "Suspension",
                    "Syrup",
                    "Oral Sachet",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Strip of 10",
                    "Strip of 20",
                    "Bottle of 30",
                    "Bottle of 60",
                    "100ml Bottle",

                ],

                # Common indications
                "indications": [

                    "Acidity",
                    "GERD",
                    "Peptic Ulcer",
                    "Constipation",
                    "Diarrhea",
                    "Nausea",
                    "Vomiting",

                ],

                # Common side effects
                "side_effects": [

                    "Headache",
                    "Constipation",
                    "Diarrhea",
                    "Abdominal Pain",
                    "Nausea",

                ],

                # Contraindications
                "contraindications": [

                    "Hypersensitivity to active ingredient",
                    "Severe Liver Disease",

                ],

                # Storage instructions
                "storage": [

                    "Store below 30°C.",
                    "Protect from moisture.",
                    "Keep out of reach of children.",

                ],

            },

            # -------------------------------------------------
            # Respiratory
            # -------------------------------------------------

            "Respiratory": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Bronchodilator",

                    "Antihistamine",

                    "Leukotriene Receptor Antagonist",

                    "Mucolytic",

                ],

                # Available strengths
                "strengths": [

                    "5mg",
                    "10mg",
                    "20mg",
                    "250mg/5ml",
                    "500mg/5ml",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Tablet",

                    "Capsule",

                    "Syrup",

                    "Suspension",

                    "Inhaler",

                    "Respules",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Strip of 10",

                    "Bottle of 60",

                    "Bottle of 100",

                    "60ml Bottle",

                    "100ml Bottle",

                ],

                # Common indications
                "indications": [

                    "Asthma",

                    "COPD",

                    "Seasonal Allergy",

                    "Allergic Rhinitis",

                    "Dry Cough",

                    "Productive Cough",

                ],

                # Common side effects
                "side_effects": [

                    "Headache",

                    "Dry Mouth",

                    "Dizziness",

                    "Palpitations",

                    "Drowsiness",

                ],

                # Contraindications
                "contraindications": [

                    "Hypersensitivity to active ingredient",

                    "Severe Respiratory Depression",

                ],

                # Storage instructions
                "storage": [

                    "Store below 30°C.",

                    "Protect from direct sunlight.",

                    "Keep out of reach of children.",

                ],

            },

            # -------------------------------------------------
            # Vitamins & Supplements
            # -------------------------------------------------

            "Vitamins": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Vitamin Supplement",

                    "Mineral Supplement",

                    "Iron Supplement",

                    "Calcium Supplement",

                    "Multivitamin",

                ],

                # Available strengths
                "strengths": [

                    "250mg",
                    "500mg",
                    "650mg",
                    "1000mg",

                    "5mg",
                    "10mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Tablet",

                    "Capsule",

                    "Syrup",

                    "Oral Sachet",

                    "Drops",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Bottle of 30",

                    "Bottle of 60",

                    "Bottle of 100",

                    "Strip of 10",

                    "Strip of 20",

                ],

                # Common indications
                "indications": [

                    "Vitamin Deficiency",

                    "Calcium Deficiency",

                    "Iron Deficiency",

                    "Immune Support",

                    "General Weakness",

                    "Pregnancy Supplements",

                ],

                # Common side effects
                "side_effects": [

                    "Constipation",

                    "Nausea",

                    "Abdominal Pain",

                    "Loss of Appetite",

                ],

                # Contraindications
                "contraindications": [

                    "Hypersensitivity to active ingredient",

                ],

                # Storage instructions
                "storage": [

                    "Store below 30°C.",

                    "Protect from moisture.",

                    "Keep out of reach of children.",

                ],

            },

            # -------------------------------------------------
            # Skin Care
            # -------------------------------------------------

            "Skin Care": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Topical Antibiotic",

                    "Topical Antifungal",

                    "Topical Corticosteroid",

                    "Topical Acne Treatment",

                    "Topical Antiseptic",

                ],

                # Available strengths
                "strengths": [

                    "0.5%",

                    "1%",

                    "2%",

                    "5mg",

                    "10mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Cream",

                    "Ointment",

                    "Gel",

                    "Lotion",

                    "Spray",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Tube 10g",

                    "Tube 20g",

                    "Tube 30g",

                    "Pack of 1",

                ],

                # Common indications
                "indications": [

                    "Fungal Infection",

                    "Eczema",

                    "Dermatitis",

                    "Acne",

                    "Psoriasis",

                ],

                # Common side effects
                "side_effects": [

                    "Skin Rash",

                    "Itching",

                    "Redness",

                    "Dry Skin",

                    "Burning Sensation",

                ],

                # Contraindications
                "contraindications": [

                    "Hypersensitivity to active ingredient",

                    "Open Wounds",

                ],

                # Storage instructions
                "storage": [

                    "Store below 30°C.",

                    "Protect from direct sunlight.",

                    "Keep tightly closed.",

                ],

            },

            # -------------------------------------------------
            # Eye Care
            # -------------------------------------------------

            "Eye Care": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Ophthalmic Antibiotic",

                    "Artificial Tears",

                    "Antiglaucoma",

                    "Ophthalmic Anti-inflammatory",

                    "Antiallergic Eye Preparation",

                ],

                # Available strengths
                "strengths": [

                    "0.3%",

                    "0.5%",

                    "1%",

                    "2%",

                    "5mg/ml",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Eye Drops",

                    "Eye Ointment",

                    "Gel",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "5ml Bottle",

                    "10ml Bottle",

                    "Pack of 1",

                ],

                # Common indications
                "indications": [

                    "Conjunctivitis",

                    "Dry Eyes",

                    "Eye Allergy",

                    "Eye Infection",

                    "Glaucoma",

                ],

                # Common side effects
                "side_effects": [

                    "Blurred Vision",

                    "Eye Irritation",

                    "Burning Sensation",

                    "Redness",

                    "Itching",

                ],

                # Contraindications
                "contraindications": [

                    "Hypersensitivity to active ingredient",

                ],

                # Storage instructions
                "storage": [

                    "Store below 25°C.",

                    "Protect from direct sunlight.",

                    "Keep tightly closed.",

                ],

            },

            # -------------------------------------------------
            # ENT
            # -------------------------------------------------

            "ENT": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Nasal Decongestant",

                    "Antihistamine",

                    "Otic Antibiotic",

                    "Nasal Corticosteroid",

                    "Throat Antiseptic",

                ],

                # Available strengths
                "strengths": [

                    "0.05%",

                    "0.1%",

                    "0.5%",

                    "5mg",

                    "10mg",

                    "250mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Nasal Spray",

                    "Ear Drops",

                    "Tablet",

                    "Syrup",

                    "Lozenge",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "10ml Bottle",

                    "20ml Bottle",

                    "Strip of 10",

                    "Bottle of 60",

                ],

                # Common indications
                "indications": [

                    "Sinusitis",

                    "Sore Throat",

                    "Nasal Congestion",

                    "Ear Infection",

                    "Allergic Rhinitis",

                ],

                # Common side effects
                "side_effects": [

                    "Dry Mouth",

                    "Drowsiness",

                    "Nasal Irritation",

                    "Headache",

                    "Dizziness",

                ],

                # Contraindications
                "contraindications": [

                    "Hypersensitivity to active ingredient",

                ],

                # Storage
                "storage": [

                    "Store below 30°C.",

                    "Protect from direct sunlight.",

                    "Keep tightly closed.",

                ],

            },

            # -------------------------------------------------
            # Neurology
            # -------------------------------------------------

            "Neurology": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Antiepileptic",

                    "Neuropathic Pain Agent",

                    "Antidepressant",

                    "Anxiolytic",

                    "Anti-Migraine",

                ],

                # Available strengths
                "strengths": [

                    "5mg",

                    "10mg",

                    "25mg",

                    "50mg",

                    "75mg",

                    "100mg",

                    "150mg",

                    "300mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Tablet",

                    "Capsule",

                    "Oral Solution",

                    "Injection",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Strip of 10",

                    "Strip of 20",

                    "Bottle of 30",

                    "Bottle of 60",

                ],

                # Common indications
                "indications": [

                    "Epilepsy",

                    "Neuropathic Pain",

                    "Depression",

                    "Anxiety",

                    "Migraine",

                ],

                # Common side effects
                "side_effects": [

                    "Dizziness",

                    "Drowsiness",

                    "Fatigue",

                    "Headache",

                    "Blurred Vision",

                ],

                # Contraindications
                "contraindications": [

                    "Hypersensitivity to active ingredient",

                    "History of Seizures",

                ],

                # Storage
                "storage": [

                    "Store below 30°C.",

                    "Protect from moisture.",

                    "Keep out of reach of children.",

                ],

            },

            # -------------------------------------------------
            # Women's Health
            # -------------------------------------------------

            "Women's Health": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Iron Supplement",

                    "Prenatal Vitamin",

                    "Hormonal Therapy",

                    "Oral Contraceptive",

                    "Antifungal",

                ],

                # Available strengths
                "strengths": [

                    "5mg",

                    "10mg",

                    "100mg",

                    "200mg",

                    "400mcg",

                    "500mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Tablet",

                    "Capsule",

                    "Syrup",

                    "Vaginal Cream",

                    "Vaginal Tablet",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Strip of 10",

                    "Strip of 21",

                    "Strip of 28",

                    "Bottle of 30",

                    "Bottle of 60",

                ],

                # Common indications
                "indications": [

                    "Pregnancy Supplements",

                    "Iron Deficiency",

                    "Menstrual Pain",

                    "Hormonal Imbalance",

                    "Vaginal Fungal Infection",

                ],

                # Common side effects
                "side_effects": [

                    "Nausea",

                    "Vomiting",

                    "Constipation",

                    "Headache",

                    "Abdominal Pain",

                ],

                # Contraindications
                "contraindications": [

                    "Pregnancy (when applicable)",

                    "Breastfeeding (when applicable)",

                    "Hypersensitivity to active ingredient",

                ],

                # Storage
                "storage": [

                    "Store below 30°C.",

                    "Protect from moisture.",

                    "Keep out of reach of children.",

                ],

            },

            # -------------------------------------------------
            # Urology
            # -------------------------------------------------

            "Urology": {

                # Compatible therapeutic classes
                "therapeutic_classes": [

                    "Alpha Blocker",

                    "5-Alpha Reductase Inhibitor",

                    "Antimuscarinic",

                    "Urinary Alkalinizer",

                    "Phosphodiesterase Type 5 Inhibitor",

                ],

                # Available strengths
                "strengths": [

                    "0.4mg",

                    "0.5mg",

                    "2mg",

                    "4mg",

                    "5mg",

                    "10mg",

                    "25mg",

                ],

                # Supported dosage forms
                "dosage_forms": [

                    "Tablet",

                    "Capsule",

                    "Syrup",

                    "Oral Solution",

                ],

                # Compatible package sizes
                "package_sizes": [

                    "Strip of 10",

                    "Strip of 20",

                    "Bottle of 30",

                    "Bottle of 60",

                ],

                # Common indications
                "indications": [

                    "Benign Prostatic Hyperplasia",

                    "Overactive Bladder",

                    "Urinary Tract Infection",

                    "Kidney Stones",

                    "Erectile Dysfunction",

                ],

                # Common side effects
                "side_effects": [

                    "Dizziness",

                    "Headache",

                    "Dry Mouth",

                    "Hypotension",

                    "Nausea",

                ],

                # Contraindications
                "contraindications": [

                    "Severe Liver Disease",

                    "Severe Kidney Disease",

                    "Hypersensitivity to active ingredient",

                ],

                # Storage
                "storage": [

                    "Store below 30°C.",

                    "Protect from moisture.",

                    "Keep tightly closed.",

                ],

            },

        }    

    # ---------------------------------------------------------
    # Rule Lookup
    # ---------------------------------------------------------

    def category_rule(
        self,
        category,
    ):
        """
        Returns the compatibility rules for a category.
        """

        rules = self.category_rules()

        return deepcopy(
            rules.get(category, {})
        )
    # ---------------------------------------------------------
    # Medicine-Specific Overrides
    # ---------------------------------------------------------

    def medicine_overrides(self):
        """
        Medicine-specific compatibility rules.

        Only values that differ from the category defaults
        need to be specified here.
        """

        return {

        # =====================================================
        # Pain Relief
        # =====================================================

        "Paracetamol": {

            "therapeutic_class": "Analgesic",

            "strengths": [
                "250mg",
                "500mg",
                "650mg",
                "1000mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Syrup",
                "Suspension",
                "Drops",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
                "Bottle of 100",
                "60ml Bottle",
                "100ml Bottle",
            ],

            "indications": [
                "Headache",
                "Fever",
                "Body Pain",
                "Muscle Pain",
                "Joint Pain",
                "Dental Pain",
            ],

        },

        "Ibuprofen": {

            "therapeutic_class": "NSAID",

            "strengths": [
                "200mg",
                "400mg",
                "600mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Capsule",
                "Suspension",
                "Syrup",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
                "100ml Bottle",
            ],

            "indications": [
                "Fever",
                "Headache",
                "Migraine",
                "Joint Pain",
                "Muscle Pain",
                "Dental Pain",
            ],

        },

        "Diclofenac": {

            "therapeutic_class": "NSAID",

            "strengths": [
                "25mg",
                "50mg",
                "75mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Injection",
                "Gel",
                "Cream",
            ],

            "package_sizes": [
                "Strip of 10",
                "Tube 20g",
                "Tube 30g",
                "Ampoule",
            ],

            "indications": [
                "Joint Pain",
                "Back Pain",
                "Muscle Pain",
                "Arthritis",
            ],

        },

        "Naproxen": {

            "therapeutic_class": "NSAID",

            "strengths": [
                "250mg",
                "500mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Joint Pain",
                "Back Pain",
                "Migraine",
                "Menstrual Pain",
            ],

        },

        "Ketorolac": {

            "therapeutic_class": "NSAID",

            "strengths": [
                "10mg",
                "30mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Injection",
            ],

            "package_sizes": [
                "Strip of 10",
                "Ampoule",
            ],

            "indications": [
                "Postoperative Pain",
                "Dental Pain",
                "Severe Pain",
            ],

        },

        # =====================================================
        # Antibiotics
        # =====================================================

        "Amoxicillin": {

            "therapeutic_class": "Penicillin Antibiotic",

            "strengths": [
                "250mg",
                "500mg",
            ],

            "dosage_forms": [
                "Capsule",
                "Tablet",
                "Suspension",
            ],

            "package_sizes": [
                "Strip of 10",
                "100ml Bottle",
            ],

            "indications": [
                "Respiratory Infection",
                "Ear Infection",
                "Skin Infection",
            ],

        },

        "Co-Amoxiclav": {

            "therapeutic_class": "Penicillin Antibiotic",

            "strengths": [
                "250mg",
                "500mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Suspension",
            ],

            "package_sizes": [
                "Strip of 10",
                "100ml Bottle",
            ],

            "indications": [
                "Respiratory Infection",
                "Skin Infection",
                "Urinary Tract Infection",
            ],

        },

        "Azithromycin": {

            "therapeutic_class": "Macrolide",

            "strengths": [
                "250mg",
                "500mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Capsule",
                "Suspension",
            ],

            "package_sizes": [
                "Strip of 3",
                "Strip of 6",
                "100ml Bottle",
            ],

            "indications": [
                "Respiratory Infection",
                "Ear Infection",
                "Skin Infection",
            ],

        },

        "Clarithromycin": {

            "therapeutic_class": "Macrolide",

            "strengths": [
                "250mg",
                "500mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Suspension",
            ],

            "package_sizes": [
                "Strip of 10",
                "100ml Bottle",
            ],

            "indications": [
                "Respiratory Infection",
                "Skin Infection",
            ],

        },

        "Cefixime": {

            "therapeutic_class": "Cephalosporin",

            "strengths": [
                "200mg",
                "400mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Capsule",
                "Suspension",
            ],

            "package_sizes": [
                "Strip of 10",
                "100ml Bottle",
            ],

            "indications": [
                "Typhoid Fever",
                "Respiratory Infection",
                "Urinary Tract Infection",
            ],

        },

        "Ceftriaxone": {

            "therapeutic_class": "Cephalosporin",

            "strengths": [
                "500mg",
                "1000mg",
            ],

            "dosage_forms": [
                "Injection",
            ],

            "package_sizes": [
                "Vial",
            ],

            "indications": [
                "Respiratory Infection",
                "Typhoid Fever",
                "Bacterial Infection",
            ],

        },

        "Cefuroxime": {

            "therapeutic_class": "Cephalosporin",

            "strengths": [
                "250mg",
                "500mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Suspension",
                "Injection",
            ],

            "package_sizes": [
                "Strip of 10",
                "Vial",
            ],

            "indications": [
                "Respiratory Infection",
                "Ear Infection",
                "Skin Infection",
            ],

        },

        "Ciprofloxacin": {

            "therapeutic_class": "Fluoroquinolone",

            "strengths": [
                "250mg",
                "500mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Infusion",
            ],

            "package_sizes": [
                "Strip of 10",
                "Bottle of 100",
            ],

            "indications": [
                "Urinary Tract Infection",
                "Typhoid Fever",
                "Bacterial Infection",
            ],

        },

        "Levofloxacin": {

            "therapeutic_class": "Fluoroquinolone",

            "strengths": [
                "250mg",
                "500mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Infusion",
            ],

            "package_sizes": [
                "Strip of 10",
                "Bottle of 100",
            ],

            "indications": [
                "Respiratory Infection",
                "Urinary Tract Infection",
            ],

        },

        "Moxifloxacin": {

            "therapeutic_class": "Fluoroquinolone",

            "strengths": [
                "400mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Eye Drops",
            ],

            "package_sizes": [
                "Strip of 5",
                "Strip of 10",
            ],

            "indications": [
                "Respiratory Infection",
                "Eye Infection",
            ],

        },

        # =====================================================
        # Diabetes
        # =====================================================

        "Metformin": {

            "therapeutic_class": "Biguanide",

            "strengths": [
                "250mg",
                "500mg",
                "850mg",
                "1000mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
                "Bottle of 60",
            ],

            "indications": [
                "Type 2 Diabetes",
                "Blood Sugar Control",
            ],

        },

        "Glimepiride": {

            "therapeutic_class": "Sulfonylurea",

            "strengths": [
                "1mg",
                "2mg",
                "4mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Type 2 Diabetes",
                "Blood Sugar Control",
            ],

        },

        "Gliclazide": {

            "therapeutic_class": "Sulfonylurea",

            "strengths": [
                "30mg",
                "60mg",
                "80mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Type 2 Diabetes",
                "Blood Sugar Control",
            ],

        },

        "Sitagliptin": {

            "therapeutic_class": "DPP-4 Inhibitor",

            "strengths": [
                "25mg",
                "50mg",
                "100mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Type 2 Diabetes",
                "Blood Sugar Control",
            ],

        },

        "Empagliflozin": {

            "therapeutic_class": "SGLT2 Inhibitor",

            "strengths": [
                "10mg",
                "25mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Type 2 Diabetes",
                "Blood Sugar Control",
            ],

        },

        # =====================================================
        # Heart Care
        # =====================================================

        "Amlodipine": {

            "therapeutic_class": "Calcium Channel Blocker",

            "strengths": [
                "5mg",
                "10mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Hypertension",
                "Angina",
            ],

        },

        "Losartan": {

            "therapeutic_class": "ARB",

            "strengths": [
                "25mg",
                "50mg",
                "100mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Hypertension",
                "Heart Failure",
            ],

        },

        "Valsartan": {

            "therapeutic_class": "ARB",

            "strengths": [
                "40mg",
                "80mg",
                "160mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Hypertension",
                "Heart Failure",
            ],

        },

        "Bisoprolol": {

            "therapeutic_class": "Beta Blocker",

            "strengths": [
                "2.5mg",
                "5mg",
                "10mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Hypertension",
                "Heart Failure",
                "Arrhythmia",
            ],

        },

        "Metoprolol": {

            "therapeutic_class": "Beta Blocker",

            "strengths": [
                "25mg",
                "50mg",
                "100mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Hypertension",
                "Angina",
                "Arrhythmia",
            ],

        },

        "Rosuvastatin": {

            "therapeutic_class": "Statin",

            "strengths": [
                "5mg",
                "10mg",
                "20mg",
                "40mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "High Cholesterol",
            ],

        },

        "Atorvastatin": {

            "therapeutic_class": "Statin",

            "strengths": [
                "10mg",
                "20mg",
                "40mg",
                "80mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "High Cholesterol",
            ],

        },

        "Clopidogrel": {

            "therapeutic_class": "Antiplatelet",

            "strengths": [
                "75mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Heart Attack Prevention",
                "Stroke Prevention",
            ],

        },

        # =====================================================
        # Gastrointestinal
        # =====================================================

        "Omeprazole": {

            "therapeutic_class": "Proton Pump Inhibitor",

            "strengths": [
                "20mg",
                "40mg",
            ],

            "dosage_forms": [
                "Capsule",
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "GERD",
                "Acidity",
                "Peptic Ulcer",
            ],

        },

        "Esomeprazole": {

            "therapeutic_class": "Proton Pump Inhibitor",

            "strengths": [
                "20mg",
                "40mg",
            ],

            "dosage_forms": [
                "Capsule",
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "GERD",
                "Acidity",
                "Peptic Ulcer",
            ],

        },

        "Pantoprazole": {

            "therapeutic_class": "Proton Pump Inhibitor",

            "strengths": [
                "20mg",
                "40mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Injection",
            ],

            "package_sizes": [
                "Strip of 10",
                "Vial",
            ],

            "indications": [
                "GERD",
                "Acidity",
                "Peptic Ulcer",
            ],

        },

        "Rabeprazole": {

            "therapeutic_class": "Proton Pump Inhibitor",

            "strengths": [
                "20mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "GERD",
                "Acidity",
            ],

        },

        "Domperidone": {

            "therapeutic_class": "Dopamine Antagonist",

            "strengths": [
                "10mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Suspension",
            ],

            "package_sizes": [
                "Strip of 10",
                "100ml Bottle",
            ],

            "indications": [
                "Nausea",
                "Vomiting",
                "GERD",
            ],

        },

        # =====================================================
        # Respiratory
        # =====================================================

        "Salbutamol": {

            "therapeutic_class": "Bronchodilator",

            "strengths": [
                "2mg",
                "4mg",
                "100mcg",
            ],

            "dosage_forms": [
                "Tablet",
                "Syrup",
                "Inhaler",
                "Respules",
            ],

            "package_sizes": [
                "Strip of 10",
                "100ml Bottle",
                "Pack of 1",
            ],

            "indications": [
                "Asthma",
                "COPD",
            ],

        },

        "Montelukast": {

            "therapeutic_class": "Leukotriene Receptor Antagonist",

            "strengths": [
                "4mg",
                "5mg",
                "10mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 20",
            ],

            "indications": [
                "Asthma",
                "Seasonal Allergy",
                "Allergic Rhinitis",
            ],

        },

        "Cetirizine": {

            "therapeutic_class": "Antihistamine",

            "strengths": [
                "5mg",
                "10mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Syrup",
            ],

            "package_sizes": [
                "Strip of 10",
                "100ml Bottle",
            ],

            "indications": [
                "Seasonal Allergy",
                "Allergic Rhinitis",
            ],

        },

        "Loratadine": {

            "therapeutic_class": "Antihistamine",

            "strengths": [
                "5mg",
                "10mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Syrup",
            ],

            "package_sizes": [
                "Strip of 10",
                "100ml Bottle",
            ],

            "indications": [
                "Seasonal Allergy",
                "Allergic Rhinitis",
            ],

        },

        # =====================================================
        # Skin Care
        # =====================================================

        "Hydrocortisone": {

            "therapeutic_class": "Topical Corticosteroid",

            "strengths": [
                "0.5%",
                "1%",
            ],

            "dosage_forms": [
                "Cream",
                "Ointment",
            ],

            "package_sizes": [
                "Tube 10g",
                "Tube 20g",
                "Tube 30g",
            ],

            "indications": [
                "Eczema",
                "Dermatitis",
                "Skin Rash",
            ],

        },

        "Clotrimazole": {

            "therapeutic_class": "Topical Antifungal",

            "strengths": [
                "1%",
                "2%",
            ],

            "dosage_forms": [
                "Cream",
                "Ointment",
                "Lotion",
            ],

            "package_sizes": [
                "Tube 10g",
                "Tube 20g",
                "Tube 30g",
            ],

            "indications": [
                "Fungal Infection",
            ],

        },

        "Miconazole": {

            "therapeutic_class": "Topical Antifungal",

            "strengths": [
                "2%",
            ],

            "dosage_forms": [
                "Cream",
                "Gel",
            ],

            "package_sizes": [
                "Tube 10g",
                "Tube 20g",
            ],

            "indications": [
                "Fungal Infection",
            ],

        },

        "Mupirocin": {

            "therapeutic_class": "Topical Antibiotic",

            "strengths": [
                "2%",
            ],

            "dosage_forms": [
                "Cream",
                "Ointment",
            ],

            "package_sizes": [
                "Tube 10g",
                "Tube 20g",
            ],

            "indications": [
                "Skin Infection",
            ],

        },

        "Benzoyl Peroxide": {

            "therapeutic_class": "Anti-acne Agent",

            "strengths": [
                "2.5%",
                "5%",
                "10%",
            ],

            "dosage_forms": [
                "Gel",
                "Cream",
            ],

            "package_sizes": [
                "Tube 20g",
                "Tube 30g",
            ],

            "indications": [
                "Acne",
            ],

        },

        "Calamine": {

            "therapeutic_class": "Skin Protectant",

            "strengths": [
                "8%",
            ],

            "dosage_forms": [
                "Lotion",
            ],

            "package_sizes": [
                "100ml Bottle",
            ],

            "indications": [
                "Itching",
                "Skin Rash",
            ],

        },

        # =====================================================
        # Eye Care
        # =====================================================

        "Carboxymethylcellulose": {

            "therapeutic_class": "Ophthalmic Lubricant",

            "strengths": [
                "0.5%",
                "1%",
            ],

            "dosage_forms": [
                "Eye Drops",
            ],

            "package_sizes": [
                "10ml Bottle",
            ],

            "indications": [
                "Dry Eyes",
            ],

        },

        "Moxifloxacin Eye Drops": {

            "therapeutic_class": "Ophthalmic Antibiotic",

            "strengths": [
                "0.5%",
            ],

            "dosage_forms": [
                "Eye Drops",
            ],

            "package_sizes": [
                "5ml Bottle",
            ],

            "indications": [
                "Eye Infection",
                "Conjunctivitis",
            ],

        },

        "Tobramycin": {

            "therapeutic_class": "Ophthalmic Antibiotic",

            "strengths": [
                "0.3%",
            ],

            "dosage_forms": [
                "Eye Drops",
                "Ointment",
            ],

            "package_sizes": [
                "5ml Bottle",
                "Tube 5g",
            ],

            "indications": [
                "Eye Infection",
                "Conjunctivitis",
            ],

        },

        "Olopatadine": {

            "therapeutic_class": "Ophthalmic Antihistamine",

            "strengths": [
                "0.1%",
                "0.2%",
            ],

            "dosage_forms": [
                "Eye Drops",
            ],

            "package_sizes": [
                "5ml Bottle",
            ],

            "indications": [
                "Eye Allergy",
            ],

        },

        "Ketorolac Eye Drops": {

            "therapeutic_class": "Ophthalmic NSAID",

            "strengths": [
                "0.5%",
            ],

            "dosage_forms": [
                "Eye Drops",
            ],

            "package_sizes": [
                "5ml Bottle",
            ],

            "indications": [
                "Eye Allergy",
                "Eye Pain",
            ],

        },

        # =====================================================
        # ENT
        # =====================================================

        "Xylometazoline": {

            "therapeutic_class": "Nasal Decongestant",

            "strengths": [
                "0.05%",
                "0.1%",
            ],

            "dosage_forms": [
                "Nasal Spray",
                "Nasal Drops",
            ],

            "package_sizes": [
                "10ml Bottle",
            ],

            "indications": [
                "Nasal Congestion",
                "Sinusitis",
            ],

        },

        "Oxymetazoline": {

            "therapeutic_class": "Nasal Decongestant",

            "strengths": [
                "0.05%",
            ],

            "dosage_forms": [
                "Nasal Spray",
                "Nasal Drops",
            ],

            "package_sizes": [
                "10ml Bottle",
            ],

            "indications": [
                "Nasal Congestion",
                "Sinusitis",
            ],

        },

        "Fluticasone": {

            "therapeutic_class": "Intranasal Corticosteroid",

            "strengths": [
                "50mcg",
            ],

            "dosage_forms": [
                "Nasal Spray",
            ],

            "package_sizes": [
                "120 Dose Bottle",
            ],

            "indications": [
                "Allergic Rhinitis",
                "Seasonal Allergy",
            ],

        },

        "Cetirizine": {

            "therapeutic_class": "Antihistamine",

            "strengths": [
                "5mg",
                "10mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Syrup",
            ],

            "package_sizes": [
                "Strip of 10",
                "100ml Bottle",
            ],

            "indications": [
                "Allergic Rhinitis",
                "Seasonal Allergy",
            ],

        },

        "Amylmetacresol + Dichlorobenzyl Alcohol": {

            "therapeutic_class": "Throat Antiseptic",

            "strengths": [
                "Lozenge",
            ],

            "dosage_forms": [
                "Lozenge",
            ],

            "package_sizes": [
                "Pack of 10",
                "Pack of 20",
            ],

            "indications": [
                "Sore Throat",
            ],

        },

        # =====================================================
        # Neurology
        # =====================================================

        "Gabapentin": {

            "therapeutic_class": "Antiepileptic",

            "strengths": [
                "100mg",
                "300mg",
                "400mg",
            ],

            "dosage_forms": [
                "Capsule",
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 30",
            ],

            "indications": [
                "Neuropathic Pain",
                "Epilepsy",
            ],

        },

        "Pregabalin": {

            "therapeutic_class": "Neuropathic Pain Agent",

            "strengths": [
                "25mg",
                "50mg",
                "75mg",
                "150mg",
            ],

            "dosage_forms": [
                "Capsule",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 30",
            ],

            "indications": [
                "Neuropathic Pain",
                "Anxiety",
            ],

        },

        "Carbamazepine": {

            "therapeutic_class": "Antiepileptic",

            "strengths": [
                "100mg",
                "200mg",
                "400mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Suspension",
            ],

            "package_sizes": [
                "Strip of 10",
                "Bottle of 100ml",
            ],

            "indications": [
                "Epilepsy",
                "Neuropathic Pain",
            ],

        },

        "Sodium Valproate": {

            "therapeutic_class": "Antiepileptic",

            "strengths": [
                "200mg",
                "500mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Syrup",
            ],

            "package_sizes": [
                "Strip of 10",
                "Bottle of 100ml",
            ],

            "indications": [
                "Epilepsy",
            ],

        },

        "Amitriptyline": {

            "therapeutic_class": "Tricyclic Antidepressant",

            "strengths": [
                "10mg",
                "25mg",
                "50mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 30",
            ],

            "indications": [
                "Depression",
                "Neuropathic Pain",
            ],

        },

        "Sertraline": {

            "therapeutic_class": "SSRI Antidepressant",

            "strengths": [
                "25mg",
                "50mg",
                "100mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 30",
            ],

            "indications": [
                "Depression",
                "Anxiety",
            ],

        },

        "Escitalopram": {

            "therapeutic_class": "SSRI Antidepressant",

            "strengths": [
                "5mg",
                "10mg",
                "20mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 30",
            ],

            "indications": [
                "Depression",
                "Anxiety",
            ],

        },

        "Clonazepam": {

            "therapeutic_class": "Benzodiazepine",

            "strengths": [
                "0.25mg",
                "0.5mg",
                "1mg",
                "2mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
            ],

            "indications": [
                "Anxiety",
                "Epilepsy",
            ],

        },

        # =====================================================
        # Women's Health
        # =====================================================

        "Folic Acid": {

            "therapeutic_class": "Pregnancy Supplement",

            "strengths": [
                "400mcg",
                "5mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 30",
                "Bottle of 100",
            ],

            "indications": [
                "Pregnancy",
                "Folate Deficiency",
            ],

        },

        "Ferrous Sulfate": {

            "therapeutic_class": "Iron Supplement",

            "strengths": [
                "200mg",
                "325mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Capsule",
                "Syrup",
            ],

            "package_sizes": [
                "Strip of 30",
                "Bottle of 100ml",
            ],

            "indications": [
                "Iron Deficiency Anemia",
                "Pregnancy",
            ],

        },

        "Calcium Carbonate": {

            "therapeutic_class": "Calcium Supplement",

            "strengths": [
                "500mg",
                "600mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Chewable Tablet",
            ],

            "package_sizes": [
                "Bottle of 30",
                "Bottle of 60",
            ],

            "indications": [
                "Calcium Deficiency",
                "Pregnancy",
            ],

        },

        "Clotrimazole Vaginal": {

            "therapeutic_class": "Vaginal Antifungal",

            "strengths": [
                "100mg",
                "200mg",
                "500mg",
            ],

            "dosage_forms": [
                "Vaginal Tablet",
                "Vaginal Cream",
            ],

            "package_sizes": [
                "Pack of 3",
                "Pack of 6",
            ],

            "indications": [
                "Vaginal Candidiasis",
            ],

        },

        "Ethinyl Estradiol + Levonorgestrel": {

            "therapeutic_class": "Combined Oral Contraceptive",

            "strengths": [
                "30mcg/150mcg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Pack of 21",
                "Pack of 28",
            ],

            "indications": [
                "Contraception",
            ],

        },

        "Norethisterone": {

            "therapeutic_class": "Progestin",

            "strengths": [
                "5mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
            ],

            "indications": [
                "Menstrual Disorders",
                "Abnormal Uterine Bleeding",
            ],

        },

        # =====================================================
        # Urology
        # =====================================================

        "Tamsulosin": {

            "therapeutic_class": "Alpha-1 Blocker",

            "strengths": [
                "0.4mg",
            ],

            "dosage_forms": [
                "Capsule",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 30",
            ],

            "indications": [
                "Benign Prostatic Hyperplasia",
            ],

        },

        "Finasteride": {

            "therapeutic_class": "5-Alpha Reductase Inhibitor",

            "strengths": [
                "5mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 30",
            ],

            "indications": [
                "Benign Prostatic Hyperplasia",
            ],

        },

        "Dutasteride": {

            "therapeutic_class": "5-Alpha Reductase Inhibitor",

            "strengths": [
                "0.5mg",
            ],

            "dosage_forms": [
                "Capsule",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 30",
            ],

            "indications": [
                "Benign Prostatic Hyperplasia",
            ],

        },

        "Solifenacin": {

            "therapeutic_class": "Urinary Antispasmodic",

            "strengths": [
                "5mg",
                "10mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 10",
                "Strip of 30",
            ],

            "indications": [
                "Overactive Bladder",
            ],

        },

        "Oxybutynin": {

            "therapeutic_class": "Urinary Antispasmodic",

            "strengths": [
                "2.5mg",
                "5mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Syrup",
            ],

            "package_sizes": [
                "Strip of 10",
                "Bottle of 100ml",
            ],

            "indications": [
                "Overactive Bladder",
            ],

        },

        "Tadalafil": {

            "therapeutic_class": "PDE5 Inhibitor",

            "strengths": [
                "5mg",
                "10mg",
                "20mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 4",
                "Strip of 10",
            ],

            "indications": [
                "Erectile Dysfunction",
                "Benign Prostatic Hyperplasia",
            ],

        },

        "Sildenafil": {

            "therapeutic_class": "PDE5 Inhibitor",

            "strengths": [
                "25mg",
                "50mg",
                "100mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Strip of 4",
                "Strip of 10",
            ],

            "indications": [
                "Erectile Dysfunction",
            ],

        },

        # =====================================================
        # Vitamins & Supplements
        # =====================================================

        "Vitamin C": {

            "therapeutic_class": "Vitamin",

            "strengths": [
                "500mg",
                "1000mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Capsule",
                "Oral Sachet",
            ],

            "package_sizes": [
                "Bottle of 30",
                "Bottle of 60",
                "Bottle of 100",
            ],

            "indications": [
                "Vitamin Deficiency",
                "Immune Support",
            ],

        },

        "Vitamin D3": {

            "therapeutic_class": "Vitamin",

            "strengths": [
                "400IU",
                "1000IU",
                "2000IU",
                "5000IU",
            ],

            "dosage_forms": [
                "Tablet",
                "Capsule",
                "Drops",
            ],

            "package_sizes": [
                "Bottle of 30",
                "Bottle of 60",
            ],

            "indications": [
                "Vitamin Deficiency",
                "Calcium Deficiency",
            ],

        },

        "Calcium Carbonate": {

            "therapeutic_class": "Mineral Supplement",

            "strengths": [
                "500mg",
                "1000mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Oral Sachet",
            ],

            "package_sizes": [
                "Bottle of 30",
                "Bottle of 60",
                "Bottle of 100",
            ],

            "indications": [
                "Calcium Deficiency",
                "General Weakness",
            ],

        },

        "Ferrous Sulfate": {

            "therapeutic_class": "Iron Supplement",

            "strengths": [
                "200mg",
                "325mg",
            ],

            "dosage_forms": [
                "Tablet",
                "Syrup",
            ],

            "package_sizes": [
                "Bottle of 30",
                "Bottle of 60",
                "100ml Bottle",
            ],

            "indications": [
                "Iron Deficiency",
                "General Weakness",
            ],

        },

        "Folic Acid": {

            "therapeutic_class": "Folate Supplement",

            "strengths": [
                "400mcg",
                "5mg",
            ],

            "dosage_forms": [
                "Tablet",
            ],

            "package_sizes": [
                "Bottle of 30",
                "Bottle of 60",
            ],

            "indications": [
                "Pregnancy Supplements",
                "Iron Deficiency",
            ],

        },

    }
    # ---------------------------------------------------------
    # Lookup Override
    # ---------------------------------------------------------

    def get_override(
        self,
        generic_name,
    ):
        """
        Returns medicine-specific overrides.
        """

        overrides = self.medicine_overrides()

        return deepcopy(
            overrides.get(
                generic_name,
                {},
            )
        )
    # ---------------------------------------------------------
    # Merge Rules
    # ---------------------------------------------------------

    def merge_profile(
        self,
        category_profile,
        medicine_override,
    ):
        """
        Merge category defaults with medicine-specific rules.
        """

        profile = deepcopy(category_profile)

        for key, value in medicine_override.items():

            profile[key] = deepcopy(value)

        return profile
        # ============================================================
    # Profile Builder
    # ============================================================

    def get_category_rules(self, category: str) -> dict:
        """
        Returns compatibility rules for a category.
        """

        return self.CATEGORY_RULES.get(
            category,
            {
                "therapeutic_class": [],
                "strengths": [],
                "dosage_forms": [],
                "package_sizes": [],
            },
        )

    def get_override(
        self,
        generic_name: str,
    ) -> dict:
        """
        Returns medicine-specific overrides for a generic medicine.
        """

        overrides = self.medicine_overrides()

        return deepcopy(
            overrides.get(
                generic_name,
                {},
            )
        )

    # ------------------------------------------------------------

    def build_profile(
        self,
        medicine: dict,
    ) -> dict:
        """
        Builds one complete medicine profile by combining:

        1. Generic medicine
        2. Category compatibility rules
        3. Medicine-specific overrides

        Returns
        -------
        dict
        """

        generic_name = medicine["generic_name"]
        category = medicine["category"]

        # ---------------------------------------------------------
        # Load category defaults
        # ---------------------------------------------------------

        profile = deepcopy(
            self.category_rule(category)
        )

        # ---------------------------------------------------------
        # Apply medicine-specific overrides
        # ---------------------------------------------------------

        overrides = self.get_override(
            generic_name
        )

        profile.update(overrides)

        # ---------------------------------------------------------
        # Required identity fields
        # ---------------------------------------------------------

        profile["generic_name"] = generic_name

        profile["category"] = category

        # ---------------------------------------------------------
        # Therapeutic Classes
        # ---------------------------------------------------------

        profile["therapeutic_classes"] = self.ensure_list(
            profile.get(
                "therapeutic_classes",
                [],
            )
        )

        # ---------------------------------------------------------
        # Strengths
        # ---------------------------------------------------------

        profile["strengths"] = self.ensure_list(
            profile.get(
                "strengths",
                [],
            )
        )

        # ---------------------------------------------------------
        # Dosage Forms
        # ---------------------------------------------------------

        profile["dosage_forms"] = self.ensure_list(
            profile.get(
                "dosage_forms",
                [],
            )
        )

        # ---------------------------------------------------------
        # Package Sizes
        # ---------------------------------------------------------

        profile["package_sizes"] = self.ensure_list(
            profile.get(
                "package_sizes",
                [],
            )
        )

        # ---------------------------------------------------------
        # Indications
        # ---------------------------------------------------------

        profile["indications"] = self.ensure_list(
            profile.get(
                "indications",
                [],
            )
        )

        # ---------------------------------------------------------
        # Side Effects
        # ---------------------------------------------------------

        profile["side_effects"] = self.ensure_list(
            profile.get(
                "side_effects",
                [],
            )
        )

        # ---------------------------------------------------------
        # Contraindications
        # ---------------------------------------------------------

        profile["contraindications"] = self.ensure_list(
            profile.get(
                "contraindications",
                [],
            )
        )

        # ---------------------------------------------------------
        # Storage
        # ---------------------------------------------------------

        profile["storage"] = self.ensure_list(
            profile.get(
                "storage",
                [],
            )
        )

        return profile

    def build_profiles(
        self,
    ) -> list[dict]:
        """
        Build a complete profile for every generic medicine.
        """

        profiles = []

        for medicine in self.generic_medicines:

            profile = self.build_profile(
                medicine
            )

            profiles.append(profile)

        profiles.sort(
            key=lambda item: item["generic_name"]
        )

        return profiles
    # ------------------------------------------------------------

    def validate_profiles(self, profiles):
        """
        Basic validation.
        """

        names = set()

        for profile in profiles:

            generic = profile["generic_name"]

            if generic in names:
                raise ValueError(
                    f"Duplicate generic: {generic}"
                )

            names.add(generic)

            if not profile["strengths"]:
                raise ValueError(
                    f"{generic} has no strengths."
                )

            if not profile["dosage_forms"]:
                raise ValueError(
                    f"{generic} has no dosage forms."
                )

            if not profile["package_sizes"]:
                raise ValueError(
                    f"{generic} has no package sizes."
                )

        return profiles

    # ------------------------------------------------------------

    def generate(
        self,
    ):
        """
        Generate all medicine profiles.
        """

        profiles = self.build_profiles()

        self.data = profiles

        return profiles
    # ============================================================
# Part 5
# Export & CLI Entry Point
# ============================================================

    def generate(self):
        """
        Required by BaseGenerator.

        Builds every medicine profile and returns
        them as a list.

        BaseGenerator.export() automatically writes
        them to:

            seeders/data/medicine_profiles.json
        """

        profiles = self.build_profiles()

        print("")
        print("=" * 60)
        print("Medicine Profile Generator")
        print("=" * 60)
        print(f"Profiles generated : {len(profiles)}")
        print("=" * 60)

        return profiles

    # ---------------------------------------------------------

    def statistics(self):
        """
        Display useful statistics.
        """

        profiles = self.build_profiles()

        print("")
        print("=" * 60)
        print("Medicine Profile Statistics")
        print("=" * 60)

        print(f"Total Medicines : {len(profiles)}")

        categories = {}

        for profile in profiles:

            category = profile["category"]

            categories.setdefault(category, 0)

            categories[category] += 1

        print("")

        for category, count in sorted(categories.items()):

            print(f"{category:25} {count}")

        print("=" * 60)

    # ---------------------------------------------------------

    def preview(
        self,
        limit=5,
    ):
        """
        Preview generated profiles.
        """

        profiles = self.build_profiles()

        print("")
        print("=" * 60)
        print("Medicine Profile Preview")
        print("=" * 60)

        for profile in profiles[:limit]:

            print(profile)

            print("-" * 60)

    # ---------------------------------------------------------

    def validate_profiles(self):
        """
        Simple validation.
        """

        profiles = self.build_profiles()

        names = set()

        for profile in profiles:

            if "generic_name" not in profile:
                raise ValueError(
                    "Missing generic_name"
                )

            if "category" not in profile:
                raise ValueError(
                    "Missing category"
                )

            if profile["generic_name"] in names:

                raise ValueError(
                    f"Duplicate profile: "
                    f"{profile['generic_name']}"
                )

            names.add(
                profile["generic_name"]
            )

        print("✓ Validation passed.")

        return True


    # ============================================================
    # Convenience Helper
    # ============================================================

    def generate_medicine_profiles():
        """
        Build and export medicine profiles.

        Returns
        -------
        list
            Exported profiles.
        """

        generator = MedicineProfileGenerator()

        return generator.export()


    # ============================================================
    # CLI Entry
    # ============================================================

    if __name__ == "__main__":

        generate_medicine_profiles()