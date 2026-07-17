# Force registration
import seeders.categories
import seeders.manufacturers
import seeders.brands
import seeders.products
import seeders.inventory
import seeders.images
import seeders.reviews
import seeders.brands

from seeders.registry import SEEDERS


def run_all():
    print("=" * 60)
    print("Starting Pharmacy Seeder")
    print("=" * 60)

    for seeder in SEEDERS:
        print(f"Running {seeder.name}")
        seeder.run()

    print("=" * 60)
    print("Done")
    print("=" * 60)