from rest_framework import serializers
from services.models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
            'provider': {'required': False},
        }

