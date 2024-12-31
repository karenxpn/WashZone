from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from services.service_models.category import Category
from services.service_models.provider import Provider
from user.models import User


class SlotViewTests(APITestCase):
    def setUp(self):

        self.url = reverse('slot')

        self.user = User.objects.create_user(username='user', is_staff=True)
        self.user2 = User.objects.create_user(username='user2')
        self.category = Category.objects.create(name='unique name here')

        self.provider = Provider.objects.create(
            owner=self.user,
            category=self.category,
            name='Provider',
            address='Address',
            location=Point()
        )

        self.valid_create_slot_payload = {
            "start_time": "2024-12-21T13:00:00+04:00",
            "end_time": "2024-12-21T14:00:00+04:00",
            "provider": self.provider.id,
        }

        self.invalid_create_slot_payload = {}

        self.api_client = APIClient()

    # test close slot
    def test_create_slot_not_authenticated(self):
        response = self.api_client.post(self.url, self.valid_create_slot_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_slot_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.url, self.valid_create_slot_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_slot_not_provider(self):
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(self.url, self.valid_create_slot_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_slot_invalid_payload(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.url, self.invalid_create_slot_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # get time slots tests
    def test_get_timeslots_not_authenticated(self):
        response = self.api_client.get(self.url, {'date': '2024-12-21', 'provider': self.provider.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_timeslots_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(self.url, {'date': '2024-12-21', 'provider': self.provider.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)