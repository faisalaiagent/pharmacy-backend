"""
seeders/generators/storage_generator.py

Generates storage instruction reference dataset.

Output:
    seeders/data/storage.json
"""

from __future__ import annotations

from .base_generator import BaseGenerator


class StorageGenerator(BaseGenerator):
    """
    Generates storage instruction master data.
    """

    OUTPUT_FILE = "storage.json"

    DATA = [

        "Store below 25°C.",
        "Store below 30°C.",
        "Store in a cool and dry place.",
        "Protect from direct sunlight.",
        "Keep tightly closed.",
        "Do not freeze.",
        "Refrigerate between 2°C and 8°C.",
        "Keep out of reach of children.",
        "Protect from moisture.",
        "Store in original packaging.",

    ]

    def __init__(self):

        super().__init__()

    def generate(self):
        """
        Return storage instruction dataset.

        BaseGenerator.export() automatically writes
        the JSON file.
        """

        return self.DATA


def generate_storage_rules():
    """
    Convenience helper.
    """

    return StorageGenerator().export()


if __name__ == "__main__":

    generate_storage_rules()