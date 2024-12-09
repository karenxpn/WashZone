from rest_framework import serializers
from services.models import Service
from .service_feature_serializer import ServiceFeatureSerializer


class ServiceSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'

class ServiceUpdateSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
            'provider': {'required': False},
            'base_price': {'required': False},
            'duration_in_minutes': {'required': False},
        }

