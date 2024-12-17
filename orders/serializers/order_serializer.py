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
    service_name = serializers.ReadOnlyField(source='service.name')
    service_id = serializers.ReadOnlyField(source='service.id')
    features = OrderItemFeatureSerializer(source='order_item_features', read_only=True, many=True)

    class Meta:
        model = OrderItem
        fields = [
            'provider',
            'service_name',
            'service_id',
            'features',
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return sum(item.order_item_subtotal for item in obj.items.all())


    class Meta:
        model = Order
        fields = [
            'user',
            'status',
            'items',
            'total_price'
        ]