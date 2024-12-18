from rest_framework import serializers
from orders.order_models.order_feature import OrderFeature
from services.service_models.feature import Feature


class CreateOrderFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeature
        fields = ['feature']

    def validate_feature(self, value):
        if not Feature.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Feature does not exist.")
        return value