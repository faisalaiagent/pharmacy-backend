from seeders.base import BaseSeeder
from seeders.registry import register
from seeders.seeders.product_seeder import ProductSeeder as _ProductSeederImpl


@register
class ProductSeeder(BaseSeeder):
    """
    Wires the real product-generation logic (seeders/seeders/product_seeder.py)
    into the run_all() pipeline. This file was previously empty, which is why
    brands were created but no actual Product records ever appeared.
    """

    name = "Product Seeder"

    def run(self):
        seeder = _ProductSeederImpl()
        seeder.seed()
