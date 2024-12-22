from django.contrib.gis.geos import Point
from django.core.management import BaseCommand

from services.service_models.feature import ServiceFeature
from .seed_feature import create_feature
from .seed_provider import create_provider
from .seed_service import create_service
from .seed_user import create_user

class Command(BaseCommand):
    help = "Seed the database with initial data."



    def handle(self, *args, **options):
        # create user
        create_user(phone_number='+37493936313')
        create_user(phone_number='+37433988988')

        #create provider
        provider1 = create_provider(1, 1,
                                    'Detroit Detailing',
                                    'ДЕТЕЙЛИНГ | ОКЛЕЙКА | ЗАЩИТНЫЕ ПОКРЫТИЯ | ХИМЧИСТКА | ЕРЕВАН\nПрофессиональный детейлинг центр в Армении🇦🇲\n🔺Автомойка | Химчистка | Полировка\n🔺Оклейка PPF и винила | Тонировка\n🔺Защитные покрытия | 📞 077 087771',
                                    '3rd backstreet, Masis St, Yerevan 0061',
                                    '077 066019',
                                    Point())

        provider2 = create_provider(1, 1,
                                    'Carlife Detailing',
                                    'Детейлинг полировка кузова.\nКерамика кузова.\nОригинальные пленки (Hexis Bodyfence)',
                                    'Armenia Yerevan Admiral-Isakov 140',
                                    '099 222264',
                                    Point())

        provider3 = create_provider(1, 1,
                                    'EG detailing center',
                                    'Մեքենան ևս խնամքի կարիք ունի',
                                    'Amiryan 4/6, Yerevan, Armenia',
                                    '+374-99-878008',
                                    Point(float(44.510154), float(40.179543)))

        # create services
        service1 = create_service(provider1, 1,
                                  'Ceramics',
                                  '',
                                  400000,
                                  5760)

        service2 = create_service(provider1, 1,
            'Detailing Carwash',
            '',
            19000,
            duration=120
        )

        service3 = create_service(provider2, 1,
                                  'Basic CarWash',
                                  '',
                                  10000,
                                  40)

        service4 = create_service(provider2, 1,
                                  'Detailing Carwash',
                                  '',
                                  17000,
                                  duration=120)

        service3 = create_service(provider3, 1,
                                  'Basic CarWash',
                                  '',
                                  8000,
                                  40)

        service4 = create_service(provider3, 1,
                                  'Detailing Carwash',
                                  '',
                                  15000,
                                  duration=120)



        # create features
        feature1 = create_feature(1,
                                  'Headlight Restoration',
                                  'Cleaning and polishing foggy or scratched headlights',
                                  20000)

        feature2 = create_feature(1,
                                  'Wax Coating',
                                  'The whole car will be wax coated for hydrofobe',
                                  20000)

        feature3 = create_feature(1,
                                  'Weel blackening',
                                  'The wheels will be blacked (satin, glyanc)',
                                  1000)



        ServiceFeature.objects.create(owner_id=1,
                                      service=service1,
                                      feature=feature1,
                                      is_included=True)

        ServiceFeature.objects.create(owner_id=1,
                                      service=service1,
                                      feature=feature2,
                                      is_included=True)

        ServiceFeature.objects.create(owner_id=1,
                                      service=service1,
                                      feature=feature3,
                                      is_included=True)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))