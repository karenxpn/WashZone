import phonenumbers
from rest_framework import serializers


def phone_number_validator(value):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(value)

        # Validate the number
        if not phonenumbers.is_valid_number(parsed_number):
            raise serializers.ValidationError("The phone number entered is not valid.")
    except phonenumbers.NumberParseException as e:
        raise serializers.ValidationError("Invalid phone number format.")

    # If valid, return the normalized E.164 format
    return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)