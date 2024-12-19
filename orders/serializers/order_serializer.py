from rest_framework import serializers

from orders.order_models.order import Order
from orders.order_models.order_feature import OrderFeature


class OrderFeatureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='feature.id')
    name = serializers.CharField(source='feature.name')
    description = serializers.CharField(source='feature.description')

    class Meta:
        model = OrderFeature
        fields = ['id', 'name', 'description', 'extra_cost', 'extra_duration']


class OrderSerializer(serializers.ModelSerializer):
    features = OrderFeatureSerializer(source='order_features', many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'owner',
            'provider',
            'service',
            'status',
            'features',
            'order_total',
            'order_duration'
        ]