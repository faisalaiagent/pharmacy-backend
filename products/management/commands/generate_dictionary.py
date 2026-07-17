"""
Django Management Command

Generate Pharmacy Medicine Dictionary

Usage
-----

python manage.py generate_dictionary

python manage.py generate_dictionary --count 1000

python manage.py generate_dictionary --count 5000

python manage.py generate_dictionary --count 10000

python manage.py generate_dictionary --no-csv

python manage.py generate_dictionary --no-json
"""

from django.core.management.base import BaseCommand

from seeders.generators.medicine_generator import MedicineGenerator


class Command(BaseCommand):

    help = "Generate production medicine dictionary"

    def add_arguments(self, parser):

        parser.add_argument(

            "--count",

            type=int,

            default=1000,

            help="Number of medicines to generate",

        )

        parser.add_argument(

            "--no-json",

            action="store_true",

            help="Disable JSON export",

        )

        parser.add_argument(

            "--no-csv",

            action="store_true",

            help="Disable CSV export",

        )

    def handle(self, *args, **options):

        count = options["count"]

        export_json = not options["no_json"]

        export_csv = not options["no_csv"]

        self.stdout.write("")

        self.stdout.write("=" * 70)

        self.stdout.write("AI Pharmacy Dictionary Generator")

        self.stdout.write("=" * 70)

        self.stdout.write(f"Requested Medicines : {count}")

        self.stdout.write(f"Export JSON         : {export_json}")

        self.stdout.write(f"Export CSV          : {export_csv}")

        self.stdout.write("=" * 70)

        generator = MedicineGenerator(

            count=count,

            export_json=export_json,

            export_csv=export_csv,

        )

        medicines = generator.generate()

        self.stdout.write("")

        self.stdout.write(

            self.style.SUCCESS(

                f"Successfully generated {len(medicines)} medicines."

            )

        )

        self.stdout.write("=" * 70)