from rest_framework import serializers

from orders.order_models.order import Order
from orders.order_models.order_feature import OrderFeature
from orders.serializers.time_slot_serializer import TimeSlotSerializer
from services.serializers.provider_serializer import ProviderSerializer


class OrderFeatureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='feature.id')
    name = serializers.CharField(source='feature_name')
    description = serializers.CharField(source='feature_description')

    class Meta:
        model = OrderFeature
        fields = ['id', 'name', 'description', 'extra_cost', 'extra_duration']


class OrderServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='service.id')
    name = serializers.CharField(source='service_name')
    description = serializers.CharField(source='service_description')
    base_price = serializers.CharField(source='service_price')
    duration = serializers.CharField(source='service_duration')

    class Meta:
        model = Order
        fields = ['id', 'name', 'description', 'base_price', 'duration']


class OrderSerializer(serializers.ModelSerializer):
    features = OrderFeatureSerializer(source='order_features', many=True, read_only=True)
    service = OrderServiceSerializer(source='*', many=False, read_only=True)
    provider = ProviderSerializer()
    time_slot = TimeSlotSerializer()

    class Meta:
        model = Order
        fields = [
            'id',
            'owner',
            'provider',
            'time_slot',
            'service',
            'status',
            'features',
            'order_total',
            'order_duration'
        ]