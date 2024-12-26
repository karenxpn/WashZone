from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from services.service_models.category import Category
from services.service_models.feature import Feature
from services.service_models.provider import Provider
from services.service_models.service import Service
from user.models import User


class ServiceViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user')
        self.user2 = User.objects.create_user(username='user2')
        self.category = Category.objects.create(name='unique name here')

        self.provider = Provider.objects.create(
            owner=self.user,
            category=self.category,
            name='test provider',
            address='test address',
            location=Point()
        )

        self.service = Service.objects.create(
            owner=self.user,
            provider=self.provider,
            name='test service',
            base_price=1000,
            duration_in_minutes=20
        )

        self.feature = Feature.objects.create(
            owner=self.user,
            name='Feature 1',
            description='Feature description',
            cost=2000
        )

        self.valid_create_payload = {
            'provider': self.provider.id,
            'name': 'valid service payload name',
            'base_price': 10000,
            'duration_in_minutes': 20,
        }

        self.invalid_create_payload = {}

        self.valid_update_payload = {
            'name': 'valid service updated payload name',
        }
        self.invalid_update_payload = {
            'name': ''
        }

        self.add_feature_valid_payload = {
            'feature_id': self.feature.id
        }

        self.add_feature_invalid_payload = {}

        self.api_client = APIClient()

    # test get services list
    def test_get_services_not_authenticated(self):
        response = self.api_client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_services_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # get one service tests
    def test_get_service_not_authenticated(self):
        response = self.api_client.get(reverse('service-detail', kwargs={'pk': self.service.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_service_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('service-detail', kwargs={'pk': self.service.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    # create service tests
    def test_create_service_not_authenticated(self):
        response = self.api_client.post(reverse('service-list'), data=self.valid_create_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_service_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('service-list'), data=self.valid_create_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_service_invalid_payload(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('service-list'), data=self.invalid_create_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_service_different_owners(self):
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(reverse('service-list'), data=self.valid_create_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # update service tests
    def test_update_service_not_authenticated(self):
        response = self.api_client.patch(reverse('service-detail', kwargs={'pk': self.service.pk}), self.valid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_service_different_owners(self):
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.patch(reverse('service-detail', kwargs={'pk': self.service.pk}), self.valid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_service_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.patch(reverse('service-detail', kwargs={'pk': self.service.pk}), self.valid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_service_invalid_payload(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.patch(reverse('service-detail', kwargs={'pk': self.service.pk}),
                                         self.invalid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # delete service tests
    def test_delete_service_not_authenticated(self):
        response = self.api_client.delete(reverse('service-detail', kwargs={'pk': self.service.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_service_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.delete(reverse('service-detail', kwargs={'pk': self.service.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_service_not_owner(self):
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.delete(reverse('service-detail', kwargs={'pk': self.service.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # get provider services tests
    def test_get_provider_services_not_authenticated(self):
        response = self.api_client.get(reverse('service-list'), {'provider_id': self.provider.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_provider_services_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('service-list'), {'provider_id': self.provider.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # get additional features tests
    def test_get_additional_features_not_authenticated(self):
        response = self.api_client.get(reverse('service-additional-features', kwargs={'pk': self.service.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_additional_features_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('service-additional-features', kwargs={'pk': self.service.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_additional_features_not_found(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('service-additional-features', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # add feature to service tests
    def test_add_feature_not_authenticated(self):
        response = self.api_client.post(reverse('service-add-feature', kwargs={'pk': self.feature.pk}),
                                       self.add_feature_valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_feature_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('service-add-feature', kwargs={'pk': self.feature.pk}),
                                       self.add_feature_valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_feature_invalid_payload(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('service-add-feature', kwargs={'pk': self.feature.pk}),
                                       self.add_feature_invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_feature_not_owner(self):
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(reverse('service-add-feature', kwargs={'pk': self.feature.pk}),
                                       self.add_feature_valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)









