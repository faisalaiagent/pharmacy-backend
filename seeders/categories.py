import json
from pathlib import Path

from django.utils.text import slugify

from products.models import Category

from seeders.base import BaseSeeder
from seeders.registry import register
from seeders.exporters import export_csv


@register
class CategorySeeder(BaseSeeder):

    name = "Category Seeder"

    def run(self):

        json_file = (
            Path(__file__).parent
            / "data"
            / "categories.json"
        )

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        exported_rows = []

        order = 1

        for item in data:

            parent, created = Category.objects.update_or_create(

                slug=slugify(item["name"]),

                defaults={
                    "name": item["name"],
                    "description": f"{item['name']} products",
                    "icon": item.get("icon", ""),
                    "image": item.get("image", ""),
                    "is_featured": item.get("featured", False),
                    "display_order": order,
                    "meta_title": item["name"],
                    "meta_description": f"Buy {item['name']} online in Pakistan.",
                },
            )

            exported_rows.append({
                "Name": parent.name,
                "Slug": parent.slug,
                "Parent": "",
                "Featured": parent.is_featured,
            })

            print(f"✓ {parent.name}")

            child_order = 1

            for child_name in item["children"]:

                child, _ = Category.objects.update_or_create(

                    slug=slugify(child_name),

                    defaults={
                        "name": child_name,
                        "parent": parent,
                        "description": f"{child_name} products",
                        "display_order": child_order,
                        "meta_title": child_name,
                        "meta_description": f"Buy {child_name} online in Pakistan.",
                    },
                )

                exported_rows.append({
                    "Name": child.name,
                    "Slug": child.slug,
                    "Parent": parent.name,
                    "Featured": child.is_featured,
                })

                print(f"   └── {child.name}")

                child_order += 1

            order += 1

        export_csv("categories", exported_rows)

        print(f"\nCreated/Updated {len(exported_rows)} categories.")