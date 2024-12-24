from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import User


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('admin')
        self.user = User.objects.create_user('user')

        self.api_client = APIClient()


    def test_get_categories_not_authorized(self):
        response = self.api_client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_categories_authorized(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_category_unauthorized(self):
        payload = {'name': 'test'}
        response = self.api_client.post(reverse('category-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_authorized_admin(self):
        payload = {'name': 'test'}
        self.api_client.force_authenticate(user=self.superuser)
        response = self.api_client.post(reverse('category-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_authorized_user(self):
        payload = {'name': 'test'}
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('category-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_invalid_payload(self):
        payload = {'name': ''}
        self.api_client.force_authenticate(user=self.superuser)
        response = self.api_client.post(reverse('category-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)