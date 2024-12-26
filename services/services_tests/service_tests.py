from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from services.service_models.category import Category
from services.service_models.provider import Provider
from services.service_models.service import Service
from user.models import User


class ServiceViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user')
        self.user2 = User.objects.create_user(username='user2')
        self.category = Category.objects.create(name='unique name here')

        self.provider = Provider.objects.create(owner=self.user,
                                                category=self.category,
                                                name='test provider',
                                                address='test address',
                                                location=Point())

        self.service = Service.objects.create(
            owner=self.user,
            provider=self.provider,
            name='test service',
            base_price=1000,
            duration_in_minutes=20
        )


        self.api_client = APIClient()

    # test get services list
    def test_get_services_not_authenticated(self):
        response = self.api_client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_services_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)