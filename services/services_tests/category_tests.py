from unicodedata import category

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from services.service_models.category import Category
from user.models import User


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('admin')
        self.user = User.objects.create_user('user')
        self.category = Category.objects.create(name='unique name here')

        self.api_client = APIClient()

    # get category list tests
    def test_get_categories_not_authenticated(self):
        response = self.api_client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_categories_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # create category tests
    def test_create_category_not_authenticated(self):
        payload = {'name': 'test'}
        response = self.api_client.post(reverse('category-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_authorized_admin(self):
        payload = {'name': 'test create'}
        self.api_client.force_authenticate(user=self.superuser)
        response = self.api_client.post(reverse('category-list'), data=payload, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_authenticated_user(self):
        payload = {'name': 'test'}
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('category-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_invalid_payload(self):
        payload = {'name': ''}
        self.api_client.force_authenticate(user=self.superuser)
        response = self.api_client.post(reverse('category-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ## update category tests
    def test_update_category_not_authenticated(self):
        payload = {'name': 'test'}
        response = self.api_client.put(reverse('category-detail', kwargs={'pk': 1}), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_category_authenticated_user(self):
        payload = {'name': 'test'}
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.patch(reverse('category-detail', kwargs={'pk': 1}), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_authorized_admin(self):
        payload = {'name': 'test'}
        self.api_client.force_authenticate(user=self.superuser)
        response = self.api_client.put(reverse('category-detail', kwargs={'pk': self.category.pk}), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_invalid_payload(self):
        payload = {'name': ''}
        self.api_client.force_authenticate(user=self.superuser)
        response = self.api_client.put(reverse('category-detail', kwargs={'pk': self.category.pk}), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # delete category
    def test_delete_category_not_authenticated(self):
        response = self.api_client.delete(reverse('category-detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_category_authenticated_user(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.delete(reverse('category-detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_authorized_admin(self):
        self.api_client.force_authenticate(user=self.superuser)
        response = self.api_client.delete(reverse('category-detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

