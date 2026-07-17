from django.core.management.base import BaseCommand

from seeders.run_all import run_all

class Command(BaseCommand):

    help = "Generate pharmacy seed data"

    def handle(self,*args,**kwargs):

        run_all()

        self.stdout.write(
            self.style.SUCCESS(
                "Database seeded successfully."
            )
        )