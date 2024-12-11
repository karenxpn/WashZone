from django.contrib.gis.geos import Point
from rest_framework import serializers


def validate_location(self, data):
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude is not None and longitude is not None:
        if not (-90 <= latitude <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        if not (-180 <= longitude <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180.")

        data['location'] = Point(longitude, latitude)

    if (latitude is not None and longitude is None) or (latitude is None and longitude is not None):
        raise serializers.ValidationError('Latitude or longitude is missing.')

    return data