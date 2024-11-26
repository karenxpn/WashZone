from rest_framework import serializers
import phonenumbers

class SendOtpBodySerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def run_validation(self, data):
        try:
            # Run the standard validation logic
            return super().run_validation(data)
        except serializers.ValidationError as exc:
            # Customize the error format
            first_error = next(iter(exc.detail.values()))
            if isinstance(first_error, list):
                first_error = first_error[0]
            raise serializers.ValidationError({"message": str(first_error)})

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

