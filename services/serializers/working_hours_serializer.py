from rest_framework import serializers
from services.service_models.provider import WorkingHour


class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = ['weekday', 'opening_time', 'closing_time']
