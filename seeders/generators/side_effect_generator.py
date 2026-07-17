"""
seeders/generators/side_effect_generator.py

Generates side effect reference dataset.

Output:
    seeders/data/side_effects.json
"""

from __future__ import annotations

from .base_generator import BaseGenerator


class SideEffectGenerator(BaseGenerator):
    """
    Generates side effect master data.
    """

    OUTPUT_FILE = "side_effects.json"

    DATA = [

        "Nausea",
        "Vomiting",
        "Diarrhea",
        "Constipation",
        "Headache",
        "Dizziness",
        "Drowsiness",
        "Dry Mouth",
        "Abdominal Pain",
        "Loss of Appetite",
        "Skin Rash",
        "Itching",
        "Redness",
        "Blurred Vision",
        "Fatigue",
        "Insomnia",
        "Palpitations",
        "Hypotension",
        "Hypertension",
        "Sweating",
        "Weight Gain",
        "Weight Loss",
        "Muscle Pain",
        "Joint Pain",
        "Liver Enzyme Elevation",
        "Kidney Function Changes",
        "Allergic Reaction",
        "Anaphylaxis",
        "Photosensitivity",
        "Injection Site Pain",

    ]

    def __init__(self):

        super().__init__()

    def generate(self):
        """
        Return side effect dataset.

        BaseGenerator.export() automatically writes
        the JSON file.
        """

        return self.DATA


def generate_side_effects():
    """
    Convenience helper.
    """

    return SideEffectGenerator().export()


if __name__ == "__main__":

    generate_side_effects()