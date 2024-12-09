from rest_framework import serializers
from services.models import Feature

class FeatureSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')  # Ensure the owner is read-only

    class Meta:
        model = Feature
        fields = '__all__'

class FeatureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
        extra_kwargs = {
            'owner': {'required': False},
            'name': {'required': False},
        }