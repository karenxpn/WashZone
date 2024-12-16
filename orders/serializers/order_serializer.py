from rest_framework import serializers

from orders.order_models.order import Order
from orders.order_models.order_item import OrderItem
from orders.order_models.order_item_feature import OrderItemFeature
from services.serializers.provider_serializer import ProviderSerializer
from services.serializers.service_serializer import ServiceSerializer

class OrderItemFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemFeature
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    features = OrderItemFeatureSerializer(read_only=True, many=True)

    class Meta:
        model = OrderItem
        fields = [
            'total_price',
            'provider',
            'service',
            'features',
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'user',
            'status',
            'order_items',
        ]