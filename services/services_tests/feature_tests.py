from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from services.service_models.feature import Feature
from user.models import User


class FeatureViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.user2 = User.objects.create_user(username='test2')

        self.feature = Feature.objects.create(
            owner=self.user,
            name='Feature 1',
            description='Feature description',
            cost=2000
        )

        self.api_client = APIClient()


    # test get features list
    def test_get_features_not_authenticated(self):
        response = self.api_client.get(reverse('feature-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_features_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('feature-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

