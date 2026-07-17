import csv
from pathlib import Path

from products.models import Brand, Manufacturer

from seeders.base import BaseSeeder
from seeders.registry import register
from seeders.exporters import export_csv


@register
class BrandSeeder(BaseSeeder):

    name = "Brand Seeder"

    def run(self):

        csv_file = (
            Path(__file__).parent
            / "data"
            / "brands.csv"
        )

        if not csv_file.exists():
            print("brands.csv not found.")
            return

        created = 0
        updated = 0

        exported = []

        print()

        with open(csv_file, newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                manufacturer = Manufacturer.objects.filter(
                    name=row["manufacturer"]
                ).first()

                brand, was_created = Brand.objects.update_or_create(

                    name=row["name"],

                    defaults={

                        "manufacturer": manufacturer,

                        "description": row["description"],

                        "logo": row.get("logo") or "",

                        "is_active": True,

                    },
                )

                if was_created:
                    created += 1
                    symbol = "✓ Created"
                else:
                    updated += 1
                    symbol = "↺ Updated"

                print(f"{symbol}: {brand.name}")

                exported.append({

                    "Manufacturer": manufacturer.name if manufacturer else "",

                    "Brand": brand.name,

                    "Description": brand.description,

                })

        export_csv("brands", exported)

        print()

        print("=" * 60)
        print(f"Created : {created}")
        print(f"Updated : {updated}")
        print(f"Total   : {len(exported)}")
        print("=" * 60)