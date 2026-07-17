"""
products.management.commands.generate_reference_data

Generates every reference dataset required by the AI Pharmacy project.

Usage
-----

python manage.py generate_reference_data

Optional

python manage.py generate_reference_data --force
"""

from pathlib import Path

from django.core.management.base import BaseCommand

from seeders.generators.strength_generator import StrengthGenerator
from seeders.generators.generic_name_generator import GenericNameGenerator
from seeders.generators.therapeutic_generator import TherapeuticGenerator
from seeders.generators.dosage_generator import DosageGenerator
from seeders.generators.package_generator import PackageGenerator
from seeders.generators.indication_generator import IndicationGenerator
from seeders.generators.side_effect_generator import SideEffectGenerator
from seeders.generators.contraindication_generator import (
    ContraindicationGenerator,
)
from seeders.generators.storage_generator import StorageGenerator
from seeders.generators.brand_generator import BrandGenerator


class Command(BaseCommand):

    help = "Generate all pharmacy reference datasets."

    DATA_DIR = (
        Path(__file__).resolve().parents[4]
        / "seeders"
        / "data"
    )

    def add_arguments(self, parser):

        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing datasets.",
        )

    # ---------------------------------------------------------

    def handle(self, *args, **options):

        force = options["force"]

        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write("AI Pharmacy Reference Dataset Generator")
        self.stdout.write("=" * 70)

        self.generate_dataset(
            "therapeutic_classes.json",
            TherapeuticGenerator(),
            force,
        )

        self.generate_dataset(
            "strengths.json",
            StrengthGenerator(),
            force,
        )

        self.generate_dataset(
            "dosage_forms.json",
            DosageGenerator(),
            force,
        )

        self.generate_dataset(
            "package_sizes.json",
            PackageGenerator(),
            force,
        )

        self.generate_dataset(
            "indications.json",
            IndicationGenerator(),
            force,
        )

        self.generate_dataset(
            "side_effects.json",
            SideEffectGenerator(),
            force,
        )

        self.generate_dataset(
            "contraindications.json",
            ContraindicationGenerator(),
            force,
        )

        self.generate_dataset(
            "storage.json",
            StorageGenerator(),
            force,
        )

        self.generate_dataset(
            "generic_names.json",
            GenericNameGenerator(),
            force,
        )

        self.generate_dataset(
            "brands.json",
            BrandGenerator(),
            force,
        )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✓ All datasets generated"))
        self.stdout.write("=" * 70)

    # ---------------------------------------------------------

    def generate_dataset(
        self,
        filename,
        generator,
        force=False,
    ):

        file_path = self.DATA_DIR / filename

        if (
            file_path.exists()
            and file_path.stat().st_size > 0
            and not force
        ):
            self.stdout.write(
                self.style.WARNING(
                    f"Skipping {filename} (already exists)"
                )
            )
            return

        self.stdout.write(
            f"Generating {filename}..."
        )

        try:

            generator.export()

            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ {filename}"
                )
            )

        except Exception as exc:

            self.stdout.write(
                self.style.ERROR(
                    f"✗ {filename}: {exc}"
                )
            )