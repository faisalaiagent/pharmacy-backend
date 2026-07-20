from django.core.management.base import BaseCommand
from products.models import Product, ProductImage


COLOR_MAP = {
    "Tablet": "0ea5e9",
    "Capsule": "14b8a6",
    "Syrup": "8b5cf6",
    "Injection": "ef4444",
}


class Command(BaseCommand):
    help = "Generate placeholder product images for every Product missing one."

    def handle(self, *args, **kwargs):
        count = 0

        for product in Product.objects.all():
            if product.images.exists():
                continue

            color = COLOR_MAP.get(product.dosage_form, "6366f1")
            name = product.name.replace(" ", "+")
            strength = (product.strength or "").replace(" ", "").replace("/", "-")
            url = (
                f"https://placehold.co/500x500/{color}/ffffff/png"
                f"?font=roboto&text={name}+{strength}"
            )

            ProductImage.objects.create(
                product=product,
                image_url=url,
                alt_text=f"{product.name} {product.strength}",
                is_primary=True,
                display_order=0,
            )

            count += 1
            self.stdout.write(f"{count}. {product.name} -> image added")

        self.stdout.write(
            self.style.SUCCESS(f"\nDone. {count} product images created.")
        )
