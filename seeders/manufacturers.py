import json
from pathlib import Path

from products.models import Manufacturer

from seeders.base import BaseSeeder
from seeders.registry import register
from seeders.exporters import export_csv


@register
class ManufacturerSeeder(BaseSeeder):

    name = "Manufacturer Seeder"

    def run(self):

        json_file = (
            Path(__file__).parent
            / "data"
            / "manufacturers.json"
        )

        if not json_file.exists():
            print("manufacturers.json not found.")
            return

        with open(json_file, "r", encoding="utf-8") as f:
            manufacturers = json.load(f)

        exported_rows = []

        created = 0
        updated = 0

        print()

        for item in manufacturers:

            manufacturer, was_created = Manufacturer.objects.update_or_create(

                name=item["name"],

                defaults={

                    "country": item.get("country", "Pakistan"),

                    "license_number": item.get("license_number", ""),

                    "website": item.get("website", ""),

                    "logo": item.get("logo", ""),

                    "description": item.get("description", ""),

                    "is_active": True,

                },
            )

            if was_created:
                created += 1
                symbol = "✓ Created"
            else:
                updated += 1
                symbol = "↺ Updated"

            print(f"{symbol}: {manufacturer.name}")

            exported_rows.append({

                "Name": manufacturer.name,

                "Country": manufacturer.country,

                "Website": manufacturer.website,

                "License": manufacturer.license_number,

            })

        export_csv("manufacturers", exported_rows)

        print()
        print("=" * 60)
        print(f"Created : {created}")
        print(f"Updated : {updated}")
        print(f"Total   : {len(exported_rows)}")
        print("CSV exported to exports/manufacturers.csv")
        print("=" * 60)