from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.validators.additional_fields_validation import additional_fields_validation
from authentication.validators.phone_number_validation import phone_number_validator


class SendOtpBodySerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        return phone_number_validator(value)

    def validate(self, data):
        return additional_fields_validation(self, data)
