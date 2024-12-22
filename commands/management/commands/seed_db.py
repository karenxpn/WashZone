from django.contrib.gis.geos import Point
from django.core.management import BaseCommand

from .seed_provider import create_provider
from .seed_user import create_user

class Command(BaseCommand):
    help = "Seed the database with initial data."



    def handle(self, *args, **options):
        # create user
        # create_user(phone_number='+37433988988')
        create_provider(1, 1, 'Seeded Provider', 'Seeded Provider Description', Point())
        create_provider(1, 1, 'Seeded Provider 1', 'Seeded Provider Description', Point())
        create_provider(1, 1, 'Seeded Provider 2', 'Seeded Provider Description', Point())

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))