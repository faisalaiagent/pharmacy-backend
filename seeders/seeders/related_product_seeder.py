import random

from django.db import transaction

from products.models import (

    Product,

    ProductRelation,

)

from seeders.repositories.product_repository import (

    ProductRepository,

)

class RelatedProductSeeder:

    def __init__(self):

        self.repo = ProductRepository()

        self.products = self.repo.products

        self.created = 0

        self.updated = 0

        self.skipped = 0

        self.errors = []

    def same_generic(

        self,

        product,

    ):

        return [

            p

            for p in self.products

            if (

                p.id != product.id

                and

                p.generic_name == product.generic_name

            )

        ] 

    def same_category(

        self,

        product,

    ):

        category_ids = list(

            product.categories.values_list(

                "id",

                flat=True,

            )

        )

        return [

            p

            for p in self.products

            if (

                p.id != product.id

                and

                p.categories.filter(

                    id__in=category_ids

                ).exists()

            )

        ] 

    RULES = {

        "Antibiotics":

            "Vitamins",

        "Heart Care":

            "Diabetes",

        "Pain Relief":

            "Gastrointestinal",

        "Respiratory":

            "Vitamins",

    }  

    def bought_together(

        self,

        product,

    ):

        category = (

            product.categories.first()

        )

        if category is None:

            return []

        target = self.RULES.get(

            category.name

        )

        if not target:

            return []

        return [

            p

            for p in self.products

            if (

                p.id != product.id

                and

                p.categories.filter(

                    name=target

                ).exists()

            )

        ]

    @transaction.atomic
    def create_relation(

        self,

        product,

        related,

        relation_type,

        score=100,

    ):

        _, created = (

            ProductRelation.objects.update_or_create(

                product=product,

                related_product=related,

                relation_type=relation_type,

                defaults={

                    "score": score,

                },

            )

        )

        if created:

            self.created += 1

        else:

            self.updated += 1

    def seed_product(

        self,

        product,

    ):

        ###################################

        # Same Generic

        ###################################

        for p in self.same_generic(

            product

        )[:3]:

            self.create_relation(

                product,

                p,

                ProductRelation.RelationType.SAME_GENERIC,

                100,

            )

        ###################################

        # Same Category

        ###################################

        for p in random.sample(

            self.same_category(

                product

            ),

            k=min(

                3,

                len(

                    self.same_category(

                        product

                    )

                ),

            ),

        ):

            self.create_relation(

                product,

                p,

                ProductRelation.RelationType.SAME_CATEGORY,

                80,

            )

        ###################################

        # Bought Together

        ###################################

        for p in random.sample(

            self.bought_together(

                product

            ),

            k=min(

                2,

                len(

                    self.bought_together(

                        product

                    )

                ),

            ),

        ):

            self.create_relation(

                product,

                p,

                ProductRelation.RelationType.BOUGHT_TOGETHER,

                90,

            ) 

    def seed(self):

        total = len(

            self.products

        )

        for index, product in enumerate(

            self.products,

            start=1,

        ):

            print(

                f"{index}/{total} -> {product.name}"

            )

            self.seed_product(

                product

            )

        return self.summary()


    run = seed 

    def summary(self):

        return {

            "products":

                len(self.products),

            "relations":

                ProductRelation.objects.count(),

            "created":

                self.created,

            "updated":

                self.updated,

            "skipped":

                self.skipped,

            "errors":

                len(self.errors),

        } 

    def print_summary(self):

        print()

        print("=" * 50)

        print("Related Product Seeder")

        print("=" * 50)

        print(f"Products  : {len(self.products)}")

        print(f"Relations : {ProductRelation.objects.count()}")

        print(f"Created   : {self.created}")

        print(f"Updated   : {self.updated}")

        print(f"Skipped   : {self.skipped}")

        print(f"Errors    : {len(self.errors)}")

        print("=" * 50)
