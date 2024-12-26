from rest_framework import serializers
from services.models import Service
from .service_feature_serializer import ServiceFeatureSerializer


class ServiceSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.phone_number')  # Ensure the owner is read-only

    class Meta:
        model = Service
        fields = '__all__'

class CreateServiceSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.phone_number',)

    class Meta:
        model = Service
        fields = '__all__'


    def validate(self, data):
        provider_owner = data.get('provider').owner
        request = self.context.get('request')

        if provider_owner != request.user:
            raise serializers.ValidationError('Service provider and owner must match')

        return data

class ServiceListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')

    class Meta:
        model = Service
        fields = '__all__'

class ServiceUpdateSerializer(serializers.ModelSerializer):
    features = ServiceFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True},
            'name': {'required': False},
            'provider': {'required': False},
            'base_price': {'required': False},
            'duration_in_minutes': {'required': False},
        }

