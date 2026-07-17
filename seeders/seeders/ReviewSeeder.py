from random import randint
from random import choice
from random import random

from django.db import transaction
from django.db.models import Avg

from products.models import (
    Product,
    Review,
)

from users.models import User

from seeders.repositories.product_repository import (
    ProductRepository,
)

class ReviewSeeder:

    MIN_REVIEWS = 3

    MAX_REVIEWS = 8

    VERIFIED_CHANCE = 0.75

    APPROVED_CHANCE = 0.98

    def __init__(self):

        self.repo = ProductRepository()

        self.users = list(
            User.objects.all()
        )

        self.created = 0
        self.updated = 0
        self.skipped = 0
        self.errors = []

TITLES = [

    "Excellent",

    "Highly Recommended",

    "Good Medicine",

    "Works Well",

    "Very Effective",

    "Satisfied",

    "Recommended",

]

COMMENTS = [

    "Very effective medicine.",

    "Doctor recommended it and it worked well.",

    "Fast relief from symptoms.",

    "Packaging was excellent.",

    "Delivered quickly.",

    "Original medicine.",

    "No side effects so far.",

    "Would purchase again.",

    "Quality product.",

    "Worth the price.",

]

def random_rating(self):

    ratings = [

        5,5,5,5,5,

        4,4,4,

        3,

        2,

    ]

    return choice(ratings)

def review_count(self):

    return randint(

        self.MIN_REVIEWS,

        self.MAX_REVIEWS,

    )

def random_user(self):

    return choice(self.users)

def build_defaults(self, rating):

    return {

        "title": choice(self.TITLES),

        "comment": choice(self.COMMENTS),

        "is_verified_purchase":
            random() < self.VERIFIED_CHANCE,

        "is_approved":
            random() < self.APPROVED_CHANCE,

        "helpful_count":
            randint(0, 50),

        "rating": rating,

    }

@transaction.atomic
def seed_product_reviews(
    self,
    product,
):

    total = self.review_count()

    users = self.users.copy()

    for _ in range(total):

        if not users:
            break

        user = users.pop(
            randint(
                0,
                len(users)-1,
            )
        )

        rating = self.random_rating()

        Review.objects.update_or_create(

            product=product,

            user=user,

            defaults=self.build_defaults(
                rating
            ),

        )

        self.created += 1

    self.update_product_rating(
        product
    )

def update_product_rating(
    self,
    product,
):

    qs = product.reviews.filter(
        is_approved=True
    )

    avg = qs.aggregate(
        Avg("rating")
    )["rating__avg"]

    product.average_rating = round(
        avg or 0,
        2,
    )

    product.review_count = qs.count()

    product.save(
        update_fields=[
            "average_rating",
            "review_count",
        ]
    )

def seed(self):

    total = self.repo.count()

    for index, product in enumerate(

        self.repo.products,

        start=1,

    ):

        print(

            f"{index}/{total} "

            f"-> {product.name}"

        )

        self.seed_product_reviews(
            product
        )

    return self.summary()

def summary(self):

    return {

        "products":

            self.repo.count(),

        "reviews":

            Review.objects.count(),

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

    print("="*50)

    print("Review Seeder")

    print("="*50)

    print(f"Products : {self.repo.count()}")

    print(f"Reviews  : {Review.objects.count()}")

    print(f"Created  : {self.created}")

    print(f"Updated  : {self.updated}")

    print(f"Skipped  : {self.skipped}")

    print(f"Errors   : {len(self.errors)}")

    print("="*50)