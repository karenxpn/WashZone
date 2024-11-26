from rest_framework import serializers
import phonenumbers


class VerifyOTPBodySerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    otp = serializers.CharField(min_length=6, max_length=6, required=True)

    def validate_phone_number(self, value):
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

    def validate_otp(self, value):
        # Check if OTP is 6 digits and all characters are numbers
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only numeric characters.")

        if len(value) != 6:
            raise serializers.ValidationError("OTP must be exactly 6 digits.")

        return value