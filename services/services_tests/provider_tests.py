from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from services.service_models.category import Category
from services.service_models.provider import Provider
from user.models import User


class ProviderViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('user')
        self.category = Category.objects.create(name='unique name here')

        self.provider = Provider.objects.create(owner=self.user,
                                                category=self.category,
                                                name='test provider',
                                                address='test address',
                                                location=Point())

        self.valid_create_payload = {
            'owner': self.user.id,
            'category': self.category.id,
            'name': 'test provider',
            'address': 'test address',
            "latitude": 40.139402,
            "longitude": 44.5020637,
            "working_hours": []
        }

        self.invalid_create_payload = {
            'owner': self.user.id,
            'category': self.category.id,
            "working_hours": []
        }

        self.valid_update_payload = {

        }

        self.invalid_update_payload = {

        }

        self.api_client = APIClient()


    # get providers list tests
    def test_get_providers_not_authenticated(self):
        response = self.api_client.get(reverse('provider-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_providers_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('provider-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # create provider tests
    def test_create_provider_not_authenticated(self):
        response = self.api_client.post(reverse('provider-list'), data=self.valid_create_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_provider_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('provider-list'), data=self.valid_create_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_provider_invalid_payload(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('provider-list'), data=self.invalid_create_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # update provider tests
