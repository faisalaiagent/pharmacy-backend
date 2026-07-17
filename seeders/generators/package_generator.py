"""
seeders/generators/package_generator.py

Generates package size reference dataset.

Output:
    seeders/data/package_sizes.json
"""

from __future__ import annotations

from .base_generator import BaseGenerator


class PackageGenerator(BaseGenerator):
    """
    Generates package size master data.
    """

    OUTPUT_FILE = "package_sizes.json"

    DATA = [

        "Strip of 10",
        "Strip of 20",
        "Bottle of 30",
        "Bottle of 60",
        "Bottle of 100",

        "60ml Bottle",
        "100ml Bottle",
        "120ml Bottle",

        "Tube 10g",
        "Tube 20g",
        "Tube 30g",

        "Vial",
        "Ampoule",

        "Pack of 1",
        "Pack of 2",
        "Pack of 5",

    ]

    def __init__(self):

        super().__init__()

    def generate(self):
        """
        Return package size dataset.

        BaseGenerator.export() automatically writes the JSON file.
        """

        return self.DATA


def generate_package_sizes():
    """
    Helper function.
    """

    return PackageGenerator().export()


if __name__ == "__main__":

    generate_package_sizes()