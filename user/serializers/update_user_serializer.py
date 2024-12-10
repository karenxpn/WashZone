from rest_framework import serializers
from django.contrib.gis.geos import Point
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
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is not None and longitude is not None:
            if not (-90 <= latitude <= 90):
                raise serializers.ValidationError("Latitude must be between -90 and 90.")
            if not (-180 <= longitude <= 180):
                raise serializers.ValidationError("Longitude must be between -180 and 180.")

            data['location'] = Point(longitude, latitude)

        return data