from django.urls import reverse
from rest_framework import status

from user.models import User
from rest_framework.test import APITestCase, APIClient


class UserDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.url = reverse('user-detail')
        self.api_client = APIClient()


    def test_get_user_detail_unauthorized(self):
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_detail(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_detail(self):
        data = {'username': 'updateduser'}
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_detail_unauthorized(self):
        data = {'username': 'updateduser'}
        response = self.api_client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_detail_invalid_data(self):
        data = {'email': '1'}

        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user_detail_not_authorized(self):
        response = self.api_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        user_exists = User.objects.filter(username="testuser").exists()
        self.assertTrue(user_exists)

    def test_delete_user_detail(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user_exists = User.objects.filter(username="testuser").exists()
        self.assertFalse(user_exists)

