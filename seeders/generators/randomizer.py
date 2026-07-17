"""
randomizer.py

Centralized random utilities for the pharmacy generator framework.

Features
--------
✓ Seeded random generator (reproducible datasets)
✓ Safe random choice
✓ Multiple unique selections
✓ Random integers
✓ Random decimals
✓ Probability checks
✓ Future-ready weighted choices
"""

from __future__ import annotations

import random
from decimal import Decimal
from datetime import date, timedelta
from typing import Any, Sequence


class Randomizer:
    """
    Production-grade random helper.

    Every generator should use this class instead of Python's
    random module directly.
    """

    DEFAULT_SEED = 2026

    def __init__(self, seed: int | None = None):

        self.seed = seed or self.DEFAULT_SEED

        self.random = random.Random(self.seed)

    # ---------------------------------------------------------
    # Basic Selection
    # ---------------------------------------------------------

    def choice(self, items: Sequence[Any], default=None):
        """
        Safe version of random.choice().
        """

        if not items:
            return default

        return self.random.choice(list(items))

    def choices(
        self,
        items: Sequence[Any],
        k: int = 1,
        unique: bool = True,
    ):
        """
        Returns k random items.
        """

        if not items:
            return []

        items = list(items)

        if unique:

            k = min(k, len(items))

            return self.random.sample(items, k)

        return self.random.choices(items, k=k)

    # ---------------------------------------------------------
    # Numbers
    # ---------------------------------------------------------

    def randint(self, minimum: int, maximum: int):

        return self.random.randint(minimum, maximum)

    def uniform(
        self,
        minimum: float,
        maximum: float,
        precision: int = 2,
    ):

        value = self.random.uniform(minimum, maximum)

        return round(value, precision)

    def decimal(
        self,
        minimum: float,
        maximum: float,
        precision: int = 2,
    ):

        value = self.random.uniform(minimum, maximum)

        return Decimal(str(round(value, precision)))

    # ---------------------------------------------------------
    # Probability
    # ---------------------------------------------------------

    def chance(self, percent: float):
        """
        Example:

        chance(25)

        returns True about 25% of the time.
        """

        return self.random.random() * 100 <= percent

    # ---------------------------------------------------------
    # Dates
    # ---------------------------------------------------------

    def random_date(
        self,
        start: date,
        end: date,
    ):

        delta = (end - start).days

        if delta <= 0:
            return start

        return start + timedelta(
            days=self.randint(0, delta)
        )

    # ---------------------------------------------------------
    # Future Support
    # ---------------------------------------------------------

    def weighted_choice(
        self,
        items,
        weights,
    ):
        """
        Example

        weighted_choice(
            ["Tablet","Capsule"],
            [80,20]
        )
        """

        if not items:
            return None

        return self.random.choices(
            population=items,
            weights=weights,
            k=1,
        )[0]

    # ---------------------------------------------------------
    # Shuffle
    # ---------------------------------------------------------

    def shuffle(self, items):

        items = list(items)

        self.random.shuffle(items)

        return items

    # ---------------------------------------------------------
    # IDs
    # ---------------------------------------------------------

    def digits(self, length: int):

        return "".join(

            str(self.randint(0, 9))

            for _ in range(length)

        )

    def alpha(self, length: int):

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        return "".join(

            self.choice(alphabet)

            for _ in range(length)

        )

    def alphanumeric(self, length: int):

        chars = (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
        )

        return "".join(

            self.choice(chars)

            for _ in range(length)

        )

    # ---------------------------------------------------------
    # Reset Seed
    # ---------------------------------------------------------

    def reseed(self, seed: int):

        self.seed = seed

        self.random.seed(seed)

    # ---------------------------------------------------------
    # Debug
    # ---------------------------------------------------------

    def info(self):

        return {

            "seed": self.seed,

            "engine": "Python Random",

        }