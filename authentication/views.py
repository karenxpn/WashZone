import random

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User, PhoneOTP


# Create your views here.
class SendOTPView(APIView):
    def post(self, request):
        print(request.data)
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Missing phone number'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(username=phone_number)
        if created:
            user.username = f'user_{phone_number}'
            user.set_unusable_password()
            user.save()

        otp = str(random.randint(100000, 999999))
        otp_entry, created = PhoneOTP.objects.get_or_create(
            user=user,
            otp=otp
        )

        # send otp here
        print(f'OTP for {phone_number}: {otp}')
        return Response({'otp': otp}, status=status.HTTP_200_OK)
