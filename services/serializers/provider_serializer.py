from rest_framework import serializers

from WashZone.location_validation import validate_location
from services.models import Provider

class ProviderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

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
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('location', None)

        return representation

    def validate(self, data):
        return validate_location(self, data)
