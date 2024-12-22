from django.contrib.gis.geos import Point
from django.core.management import BaseCommand

from .seed_provider import create_provider
from .seed_service import create_service
from .seed_user import create_user

class Command(BaseCommand):
    help = "Seed the database with initial data."



    def handle(self, *args, **options):
        # create user
        # create_user(phone_number='+37433988988')
        provider1 = create_provider(1, 1, 'Seeded Provider', 'Seeded Provider Description', Point())
        provider2 = create_provider(1, 1, 'Seeded Provider 1', 'Seeded Provider Description', Point())


        service1 = create_service(provider1, 1, 'Basic Wash Seed', 'Basic Wash Seed description', 2000, 30)
        service2 = create_service(provider2, 1, 'Premium Seed', 'Premium Seed description', 2000, 30)


        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))