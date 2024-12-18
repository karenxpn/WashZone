from rest_framework import serializers

from orders.order_models.order import Order
from orders.order_models.order_feature import OrderFeature

class OrderFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeature
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    features = OrderFeatureSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'owner',
            'provider',
            'service',
            'status',
            'features',
            'total_price'
        ]