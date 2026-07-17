from collections import defaultdict

from products.models import Product


class ProductRepository:
    """
    Repository for Product database records.
    """

    def __init__(self):

        self.products = list(
            Product.objects.select_related(
                "brand",
                "manufacturer",
            ).prefetch_related(
                "categories"
            )
        )

        self.sku_index = {}
        self.name_index = {}
        self.slug_index = {}
        self.generic_index = defaultdict(list)
        self.brand_index = defaultdict(list)
        self.manufacturer_index = defaultdict(list)
        self.category_index = defaultdict(list)

        self._build_indexes()

    # ---------------------------------------------------------
    # Indexes
    # ---------------------------------------------------------

    def _build_indexes(self):

        for product in self.products:

            self.sku_index[product.sku] = product

            self.name_index[product.name] = product

            self.slug_index[product.slug] = product

            if product.generic_name:
                self.generic_index[
                    product.generic_name
                ].append(product)

            if product.brand:
                self.brand_index[
                    product.brand.name
                ].append(product)

            if product.manufacturer:
                self.manufacturer_index[
                    product.manufacturer.name
                ].append(product)

            for category in product.categories.all():

                self.category_index[
                    category.name
                ].append(product)

    # ---------------------------------------------------------
    # Basic
    # ---------------------------------------------------------

    def count(self):
        return len(self.products)

    def all(self):
        return self.products

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(self, sku):
        return self.sku_index.get(sku)

    def by_name(self, name):
        return self.name_index.get(name)

    def by_slug(self, slug):
        return self.slug_index.get(slug)

    def by_generic(self, generic):

        return self.generic_index.get(
            generic,
            [],
        )

    def by_brand(self, brand):

        return self.brand_index.get(
            brand,
            [],
        )

    def by_manufacturer(self, manufacturer):

        return self.manufacturer_index.get(
            manufacturer,
            [],
        )

    def by_category(self, category):

        return self.category_index.get(
            category,
            [],
        )

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    def exists(self, sku):

        return sku in self.sku_index

    # ---------------------------------------------------------
    # Lists
    # ---------------------------------------------------------

    def sku_list(self):

        return sorted(
            self.sku_index.keys()
        )

    def product_names(self):

        return sorted(
            self.name_index.keys()
        )

    def brand_names(self):

        return sorted(
            self.brand_index.keys()
        )

    def manufacturer_names(self):

        return sorted(
            self.manufacturer_index.keys()
        )

    def category_names(self):

        return sorted(
            self.category_index.keys()
        )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(self, text):

        text = text.lower()

        return [

            product

            for product in self.products

            if (
                text in product.name.lower()
                or text in product.sku.lower()
                or text in product.generic_name.lower()
            )
        ]

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def summary(self):

        return {

            "products": self.count(),

            "brands": len(
                self.brand_index
            ),

            "manufacturers": len(
                self.manufacturer_index
            ),

            "categories": len(
                self.category_index
            ),
        }
    
    