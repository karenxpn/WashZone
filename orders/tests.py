from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from user.models import User


class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user')

        self.api_client = APIClient()

    # get order tests
    def test_get_orders_not_authenticated(self):
        response = self.api_client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_orders_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
