from rest_framework import serializers
from WashZone.location_validation import validate_location
from user.models import User
import re



class UpdateUserSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'email_promotions_enabled',
            'first_name',
            'last_name',
            'notifications_enabled',
            'latitude',
            'longitude',
            'image'
        )

    # validations
    def validate_email(self, email):
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

        if not valid:
            raise serializers.ValidationError('Invalid email address')
        return email

    def validate_first_name(self, first_name):
        if first_name is not None:
            if len(first_name) < 3:
                raise serializers.ValidationError('First name must be at least 3 characters')

        return first_name

    def validate_last_name(self, last_name):
        if last_name is not None:
            if len(last_name) < 3:
                raise serializers.ValidationError('Last name must be at least 3 characters')

        return last_name

    def validate(self, data):
        return validate_location(self, data)