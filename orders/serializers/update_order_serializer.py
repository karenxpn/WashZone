from rest_framework import serializers
from orders.order_models.order import Order
from orders.serializers.order_serializer import OrderSerializer


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True},
            # time slots should be here
        }

    def to_representation(self, instance):
        return OrderSerializer(instance).data