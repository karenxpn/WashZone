import random
import os

from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User, PhoneOTP
from twilio.rest import Client

# Create your views here.
class SendOTPView(APIView):
    def post(self, request):
        try:
            phone_number = request.data.get('phone_number')
        except:
            return Response({'error': 'Missing phone number'},
                            status=status.HTTP_400_BAD_REQUEST)


        print(phone_number)
        try:
            # Check if the user already exists
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            # Create a new user if not already present
            user = User(phone_number=phone_number, username=f"user_{phone_number}")
            user.set_unusable_password()
            user.save()


        otp = str(random.randint(100000, 999999))

        otp_entry, created = PhoneOTP.objects.update_or_create(
            user=user,
            defaults={
                'otp': otp,
                'created_at': now()
            }
        )

        return Response({'otp': otp}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(phone_number=phone_number)
            otp_entry = user.otp

            if otp_entry.is_expired():
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
            if otp_entry.otp == otp:
                user.is_phone_verified = True
                user.save()
                otp_entry.delete()

                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "OTP verified successfully",
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Phone number not found"}, status=status.HTTP_404_NOT_FOUND)
        except PhoneOTP.DoesNotExist:
            return Response({"error": "No OTP found for this user"}, status=status.HTTP_404_NOT_FOUND)
