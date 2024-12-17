from rest_framework import serializers

from WashZone.location_validation import validate_location
from services.models import Provider
from django.contrib.gis.geos import Point


class ProviderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Provider
        exclude = ['location']
        extra_kwargs = {
            'email': {'required': False},
        }

    def get_latitude(self, obj):
        return obj.location.y if obj.location else None

    def get_longitude(self, obj):
        return obj.location.x if obj.location else None

    def get_distance(self, obj):
        if hasattr(obj, 'distance') and obj.distance is not None:
            return round(obj.distance.m, 2)
        return None


class CreateProviderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    latitude = serializers.FloatField(write_only=True, required=True)
    longitude = serializers.FloatField(write_only=True, required=True)

    class Meta:
        model = Provider
        fields = [
            'id', 'category', 'owner', 'name', 'description', 'address',
            'contact_number', 'email', 'latitude', 'longitude', 'rating', 'number_of_reviews'
        ]
        read_only_fields = ['id', 'rating', 'number_of_reviews']

    def create(self, validated_data):
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')

        validated_data['location'] = Point(longitude, latitude)
        return Provider.objects.create(**validated_data)


class ProviderUpdateSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)

    class Meta:
        model = Provider
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True},
            'name': {'required': False},
            'description': {'required': False},
            'address': {'required': False},
            'contact_number': {'required': False},
            'email': {'required': False},
            'rating': {'required': False},
            'number_of_reviews': {'required': False},
            'category': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
            'location': {'required': False},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('location', None)

        return representation

    def validate(self, data):
        return validate_location(self, data)
