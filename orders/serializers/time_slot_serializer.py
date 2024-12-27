from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from orders.order_models.time_slot import TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'end_time', 'is_available']


class CloseTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'end_time', 'is_available', 'provider']

    def validate(self, data):
        provider = data.get('provider')
        user = self.context.get('request').user

        if provider.owner != user:
            raise PermissionDenied('You are not the provider owner.')

        return data

    def create(self, validated_data):
        validated_data['is_available'] = False
        return super().create(validated_data)
