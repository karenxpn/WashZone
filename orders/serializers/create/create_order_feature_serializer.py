from rest_framework import serializers
from orders.order_models.order_feature import OrderFeature

class CreateOrderFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeature
        fields = ['feature', 'extra_cost']
