from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock, Mock

from twilio.base.exceptions import TwilioRestException

from user.models import User
from .otp_redis import store_otp


# Create your tests here.
class AuthenticationTests(TestCase):
    def setUp(self):
        self.phone_number = '+37493936313'
        self.otp = '123456'

        self.send_otp_url = reverse('send-otp')
        self.verify_otp_url = reverse('verify-otp')

        self.user = User.objects.create(phone_number=self.phone_number, username='test')

    def tearDown(self):
        User.objects.all().delete()


    @patch('authentication.views.Client')
    @patch('authentication.otp_redis.store_otp')
    def test_send_otp_new_user(self, mock_store_otp, mock_twilio_client):
        mock_store_otp.return_value = True
        mock_twilio_client.return_value = MagicMock()
        new_phone_number = "+37433988988"

        response = self.client.post(self.send_otp_url, {
            'phone_number': new_phone_number,
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('otp', response.data)

        # Verify a new user is created
        self.assertTrue(User.objects.filter(phone_number=new_phone_number).exists())


    @patch('authentication.views.Client')
    @patch('authentication.otp_redis.store_otp')
    def test_send_otp_existing_user(self, mock_store_otp, mock_twilio_client):
        mock_store_otp.return_value = True
        mock_twilio_client.return_value = MagicMock()

        response = self.client.post(self.send_otp_url, {
            'phone_number': self.phone_number,
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('otp', response.data)

        self.assertEqual(User.objects.filter(phone_number=self.phone_number).count(), 1)


