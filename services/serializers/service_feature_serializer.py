from rest_framework import serializers
from services.models import ServiceFeature

class ServiceFeatureSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')  # Ensure the owner is read-only
    feature_name = serializers.CharField(source='feature.name', read_only=True)
    description = serializers.CharField(source='feature.description')
    feature_id = serializers.IntegerField(source='feature.id', read_only=True)

    class Meta:
        model = ServiceFeature
        fields = (
            'id',
            'owner',
            'feature_id',
            'is_included',
            'feature_name',
            'description',
            'extra_cost',
            'created_at',
            'updated_at',
        )