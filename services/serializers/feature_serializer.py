from rest_framework import serializers
from services.models import Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class FeatureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': False},
        }