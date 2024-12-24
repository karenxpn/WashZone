import random
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.base.exceptions import TwilioRestException

from .decorators import validate_request

from user.models import User
from twilio.rest import Client

from .otp_redis import store_otp, retrieve_otp, delete_otp
from .serializers.send_otp_body_serializer import SendOtpBodySerializer
from .serializers.verify_otp_body_serializer import VerifyOTPBodySerializer


# Create your views here.
class SendOTPView(APIView):
    @validate_request(SendOtpBodySerializer)
    def post(self, request):
        print(request.data)
        validated_data = request.validated_data
        print(validated_data)
        phone_number = validated_data['phone_number']

        try:
            # Check if the user already exists
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            # Create a new user if not already present
            user = User(phone_number=phone_number, username=f"user_{phone_number}")
            user.set_unusable_password()
            user.save()


        otp = str(random.randint(100000, 999999))
        store_otp(phone_number, otp)

        # Send the OTP using Twilio
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

        try:
            # client = Client(account_sid, auth_token)
            # _ = client.messages.create(
            #     messaging_service_sid=os.environ.get('MESSAGING_SERVICE_SID'),
            #     body=f'Your OTP for Wash Zone is {otp}',
            #     to=phone_number,
            # )

            return Response({'otp': otp}, status=status.HTTP_200_OK)
        except TwilioRestException as e:
            return Response({'error': f'Failed to send OTP: {str(e)}'}, status=500)
        except Exception as e:
            return Response(
                {"error": f"Failed to send OTP: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifyOTPView(APIView):
    @validate_request(VerifyOTPBodySerializer)
    def post(self, request):
        validated_data = request.validated_data
        phone_number = validated_data['phone_number']
        otp = validated_data['otp']


        try:
            user = User.objects.get(phone_number=phone_number)

            stored_otp = retrieve_otp(phone_number)
            if not stored_otp:
                return Response({"error": "OTP expired or does not exist"}, status=400)

            if stored_otp.decode() == otp:
                user.is_phone_verified = True
                user.save()

                try:
                    for token in RefreshToken.objects.filter(user=user):
                        BlacklistedToken.objects.get_or_create(token=token)
                except Exception as e:
                    pass  # Log the error if needed

                refresh = RefreshToken.for_user(user)

                delete_otp(phone_number)
                return Response({
                    "message": "OTP verified successfully",
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "Phone number not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )