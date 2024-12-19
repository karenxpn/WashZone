from rest_framework import serializers
from services.service_models.provider import SpecialClosure


class SpecialClosureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialClosure
        fields = ['date', 'reason']