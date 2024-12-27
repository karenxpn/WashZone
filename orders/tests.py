from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from orders.order_models.order import Order
from orders.order_models.time_slot import TimeSlot
from services.service_models.category import Category
from services.service_models.feature import Feature, ServiceFeature
from services.service_models.provider import Provider, WorkingHour
from services.service_models.service import Service
from user.models import User


class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user')
        self.user2 = User.objects.create_user(username='user2')

        self.category = Category.objects.create(name='category')
        self.provider = Provider.objects.create(
            category=self.category,
            owner=self.user,
            name='Provider1',
            address='Provider address 1',
            location=Point(),
        )

        for i in range(0, 7):
            WorkingHour.objects.create(
                provider=self.provider,
                weekday=i,
                opening_time="09:00:00",
                closing_time="17:00:00",
            )

        self.service = Service.objects.create(
            owner=self.user,
            provider=self.provider,
            name='Detailing CarWash',
            base_price=18000,
            duration_in_minutes=120
        )

        self.other_provider = Provider.objects.create(
            category=self.category,
            owner=self.user2,
            name='Provider2',
            address='Provider address 2',
            location=Point()
        )

        self.other_service = Service.objects.create(
            owner=self.user2,
            provider=self.other_provider,
            name='Basic CarWash',
            base_price=4000,
            duration_in_minutes=20
        )

        self.feature = Feature.objects.create(
            owner=self.user,
            name='Feature 1',
            description='Feature description',
            cost=2000
        )

        self.service_feature = ServiceFeature.objects.create(
            owner=self.user,
            service=self.service,
            feature=self.feature,
            is_included=False,
            extra_cost=9000
        )

        self.order = Order.objects.create(
            owner=self.user,
            service=self.service,
            service_name=self.service.name,
            service_description='Service description',
            service_price = self.service.base_price,
            service_duration=self.service.duration_in_minutes,
            provider=self.provider,
            status='pending',
        )

        self.valid_payload_part = {
            'service': self.service.id,
            'provider': self.provider.id,
            'start_time': '2024-12-29T13:00:00',
            'end_time': '2024-12-29T15:00:00',
            'features': [
                {
                    'feature': self.feature.id
                }
            ]
        }

        TimeSlot.objects.create(
            provider=self.provider,
            start_time='2024-12-29T09:00:00',
            end_time='2024-12-29T11:00:00',
            is_available=False,
        )

        self.valid_create_payload = self.valid_payload_part

        self.overlay_working_hour_payload = self.valid_payload_part | {
            'start_time': '2024-12-29T16:00:00',
            'end_time': '2024-12-29T18:00:00',
        }

        self.overlay_other_time_slot_payload = self.valid_payload_part | {
            'start_time': '2024-12-29T10:00:00',
            'end_time': '2024-12-29T12:00:00',
        }

        self.different_owner_provider_and_service_payload = self.valid_payload_part | {
            'service': self.other_service.id,
        }

        self.not_valid_feature_payload = self.valid_payload_part | {
            'features': [
                {
                    'feature': 99999
                }
            ]
        }

        self.valid_update_payload = {
            'status': 'approved',
        }

        self.invalid_create_payload = {}
        self.invalid_update_payload = {}

        self.api_client = APIClient()

    # get order tests
    def test_get_orders_not_authenticated(self):
        response = self.api_client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_orders_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # get one order
    def test_get_one_order_not_authenticated(self):
        response = self.api_client.get(reverse('order-detail', kwargs={'pk': self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_one_order_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(reverse('order-detail', kwargs={'pk': self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # create order tests
    # 1. create order with not authenticated user ✅
    # 2. create order with authenticated user ✅
    # 3. create order with authenticated and invalid data ✅
    # 4. create order with time-slot that overlays the working hours ✅
    # 5. create order that overlays other busy timeslot ✅
    # 6. create order with different owners ( provider owner user1, service owner user2 ) ✅
    # 7. create order with not valid feature id ✅

    def test_create_order_not_authenticated(self):
        response = self.api_client.post(reverse('order-list'), data=self.valid_create_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('order-list'), data=self.valid_create_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_invalid_data(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('order-list'), data=self.invalid_create_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_overlay_working_hours(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('order-list'), data=self.overlay_working_hour_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_overlay_other_time_slot(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('order-list'), data=self.overlay_other_time_slot_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_different_owner_provider_and_service(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('order-list'), data=self.different_owner_provider_and_service_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_not_valid_feature(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(reverse('order-list'), data=self.not_valid_feature_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # update order tests
    def test_update_order_not_authenticated(self):
        response = self.api_client.patch(reverse('order-detail', kwargs={'pk': self.order.id}), data=self.valid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_order_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.patch(reverse('order-detail', kwargs={'pk': self.order.id}), data=self.valid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_invalid_payload(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.patch(reverse('order-detail', kwargs={'pk': self.order.id}), data=self.invalid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_not_owner(self):
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.patch(reverse('order-detail', kwargs={'pk': self.order.id}), data=self.valid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # delete order tests
    def test_delete_order_not_authenticated(self):
        response = self.api_client.delete(reverse('order-detail', kwargs={'pk': self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_order_authenticated(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.delete(reverse('order-detail', kwargs={'pk': self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order_not_owner(self):
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.delete(reverse('order-detail', kwargs={'pk': self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)






