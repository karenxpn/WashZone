from rest_framework import serializers
from services.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # Same fields but tailored for updates
        extra_kwargs = {
            'name': {'required': False},  # Make `name` optional for updates
        }
