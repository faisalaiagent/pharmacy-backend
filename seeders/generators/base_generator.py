"""
seeders/generators/base_generator.py

Base class for every dataset generator.

Responsibilities
----------------
✓ Common JSON export
✓ Automatic output directory
✓ Directory creation
✓ Pretty JSON formatting
✓ Dataset validation
✓ Statistics
✓ Logging

Every generator should inherit from this class and only implement
generate().
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path


class BaseGenerator(ABC):
    """
    Base class for all reference dataset generators.
    """

    DATA_DIR = (
        Path(__file__).resolve().parent.parent
        / "data"
    )

    # Override in subclasses
    OUTPUT_FILE = None

    def __init__(self):

        self.DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------
    # Required
    # ---------------------------------------------------------

    @abstractmethod
    def generate(self):
        """
        Must return a list or dictionary.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(self, data):

        if data is None:
            raise ValueError(
                "Generator returned None."
            )

        if not isinstance(
            data,
            (list, dict),
        ):
            raise TypeError(
                "Generator must return list or dict."
            )

        return data

    # ---------------------------------------------------------
    # Output Path
    # ---------------------------------------------------------

    @property
    def output_path(self):

        if not self.OUTPUT_FILE:
            raise ValueError(
                "OUTPUT_FILE is not defined."
            )

        return self.DATA_DIR / self.OUTPUT_FILE

    # ---------------------------------------------------------
    # Export
    # ---------------------------------------------------------

    def export(self):

        data = self.validate(
            self.generate()
        )

        with open(
            self.output_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

        print(
            f"[✓] {self.OUTPUT_FILE} "
            f"({self.count(data)} records)"
        )

        return data

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def count(data):

        if isinstance(data, list):
            return len(data)

        if isinstance(data, dict):
            return len(data)

        return 0

    def preview(self, limit=5):

        data = self.generate()

        if isinstance(data, list):

            print("\nPreview\n")

            for item in data[:limit]:
                print(item)

        elif isinstance(data, dict):

            for key, value in list(data.items())[:limit]:
                print(key, value)

    def save(self):

        """
        Alias for export().
        """

        return self.export()

    def run(self):

        """
        Alias for export().
        """

        return self.export()