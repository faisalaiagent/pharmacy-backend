"""
medicine_generator.py

Production-grade medicine dictionary generator.

Responsibilities
----------------
✓ Build medicines using MedicineBuilder
✓ Generate configurable number of medicines
✓ Remove duplicates
✓ Validate generated records
✓ Export JSON
✓ Export CSV
✓ Print generation statistics
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from seeders.generators.medicine_builder import MedicineBuilder


class MedicineGenerator:

    def __init__(
        self,
        count: int = 1000,
        export_json: bool = True,
        export_csv: bool = True,
    ):

        self.count = count

        self.export_json_enabled = export_json
        self.export_csv_enabled = export_csv

        self.builder = MedicineBuilder()

        self.output_dir = (
            Path(__file__).resolve().parent.parent / "data"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.json_file = (
            self.output_dir / "medicine_dictionary.json"
        )

        self.csv_file = (
            self.output_dir / "medicine_dictionary.csv"
        )

    # ----------------------------------------------------------
    # Duplicate Removal
    # ----------------------------------------------------------

    def remove_duplicates(self, medicines):

        unique = {}

        for medicine in medicines:

            if medicine is None:
                continue

            key = (
                medicine["product_name"],
                medicine["sku"],
            )

            unique[key] = medicine

        return list(unique.values())

    # ----------------------------------------------------------
    # Build Dataset
    # ----------------------------------------------------------

    def generate(self):

        print()

        print("=" * 70)
        print("Generating Medicine Dictionary")
        print("=" * 70)

        medicines = []

        for index in range(1, self.count + 1):

            medicine = self.builder.build()

            if medicine:

                medicines.append(medicine)

            if index % 100 == 0:

                print(
                    f"Generated {index}/{self.count}"
                )

        medicines = self.remove_duplicates(
            medicines
        )

        if self.export_json_enabled:
            self.export_json(medicines)

        if self.export_csv_enabled:
            self.export_csv(medicines)

        self.print_summary(medicines)

        return medicines

    # ----------------------------------------------------------
    # JSON Export
    # ----------------------------------------------------------

    def export_json(self, medicines):

        with open(
            self.json_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                medicines,
                file,
                indent=4,
                ensure_ascii=False,
                default=str,
            )

        print()
        print(f"JSON exported -> {self.json_file}")

    # ----------------------------------------------------------
    # CSV Export
    # ----------------------------------------------------------

    def export_csv(self, medicines):

        if not medicines:
            return

        rows = []

        for medicine in medicines:

            rows.append({

                "SKU":
                    medicine.get("sku"),

                "Product":
                    medicine.get("product_name"),

                "Generic":
                    medicine.get("generic_name"),

                "Manufacturer":

                    medicine.get(
                        "manufacturer",
                        {}
                    ).get(
                        "name",
                        "",
                    ),

                "Brand":

                    medicine.get(
                        "brand",
                        {}
                    ).get(
                        "name",
                        "",
                    ),

                "Price":

                    medicine.get("price"),

                "Sale Price":

                    medicine.get(
                        "sale_price"
                    ),

                "Stock":

                    medicine.get(
                        "stock_quantity"
                    ),

            })

        with open(

            self.csv_file,

            "w",

            newline="",

            encoding="utf-8",

        ) as file:

            writer = csv.DictWriter(

                file,

                fieldnames=rows[0].keys(),

            )

            writer.writeheader()

            writer.writerows(rows)

        print(
            f"CSV exported -> {self.csv_file}"
        )

    # ----------------------------------------------------------
    # Statistics
    # ----------------------------------------------------------

    def print_summary(self, medicines):

        print()

        print("=" * 70)

        print("Generation Complete")

        print("=" * 70)

        print(f"Requested : {self.count}")

        print(f"Generated : {len(medicines)}")

        print(f"JSON File : {self.json_file.name}")

        print(f"CSV File  : {self.csv_file.name}")

        print("=" * 70)