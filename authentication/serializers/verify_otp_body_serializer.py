from rest_framework import serializers

from authentication.validators.additional_fields_validation import additional_fields_validation
from authentication.validators.phone_number_validation import phone_number_validator


class VerifyOTPBodySerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    otp = serializers.CharField(min_length=6, max_length=6, required=True)

    def validate_phone_number(self, value):
        return phone_number_validator(value)

    def validate_otp(self, value):
        # Check if OTP is 6 digits and all characters are numbers
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only numeric characters.")
        return value

    def validate(self, data):
        return additional_fields_validation(self, data)