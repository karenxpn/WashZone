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

    # @patch('authentication.views.Client')
    # @patch('authentication.views.store_otp')
    # def test_send_otp_twilio_error(self, mock_store_otp, mock_client):
    #     mock_store_otp.return_value = True
    #     mock_instance = Mock()
    #     mock_instance.messages.create.side_effect = TwilioRestException(
    #         status=500,
    #         uri='/2010-04-01/Accounts/ACXXXXXX/Messages.json',
    #         msg='Invalid phone number',
    #         code=21211
    #     )
    #
    #     mock_client.return_value = mock_instance
    #     response = self.client.post(self.send_otp_url, {'phone_number': self.phone_number})
    #
    #     print('response', response)
    #
    #     self.assertEqual(response.status_code, 500)
    #     self.assertIn('error', response.data)
    #     self.assertIn('Failed to send OTP', response.data['error'])

    @patch('authentication.views.retrieve_otp')
    @patch('authentication.views.delete_otp')
    def test_verify_otp_success(self, mock_delete_otp, mock_retrieve_otp):
        mock_retrieve_otp.return_value = self.otp.encode('utf-8')
        mock_delete_otp.return_value = True

        response = self.client.post(self.verify_otp_url, {
            'phone_number': self.phone_number,
            'otp': self.otp
        })

        # Print response data
        print("Response status:", response.status_code)
        print("Response data:", response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)


    @patch('authentication.views.retrieve_otp')
    def test_verify_otp_invalid(self, mock_retrieve_otp):
        mock_retrieve_otp.return_value = '999999'.encode('utf-8')

        response = self.client.post(self.verify_otp_url, {
            'phone_number': self.phone_number,
            'otp': self.otp
        })

        print("Response status:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid OTP', response.data['error'])


    @patch('authentication.views.retrieve_otp')
    def test_verify_otp_expired(self, mock_retrieve_otp):
        mock_retrieve_otp.return_value = None
        response = self.client.post(self.verify_otp_url, {
            'phone_number': self.phone_number,
            'otp': self.otp
        })

        print("Response status:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('OTP expired or does not exist', response.data['error'])
