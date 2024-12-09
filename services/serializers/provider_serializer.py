from rest_framework import serializers
from services.models import Provider

class ProviderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')  # Ensure the owner is read-only

    class Meta:
        model = Provider
        fields = '__all__'
        extra_kwargs = {
            'email': {'required': False},
        }

class ProviderUpdateSerializer(serializers.ModelSerializer):
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
        }
