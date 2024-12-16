from rest_framework import serializers
from orders.order_models.order import Order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        extra_kwargs = {
            'status': {'required': False},
            # time slots should be here
        }