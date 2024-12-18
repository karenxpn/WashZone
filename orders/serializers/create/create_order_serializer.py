from rest_framework import serializers
from orders.order_models.order import Order
from orders.serializers.create.create_order_feature_serializer import CreateOrderFeatureSerializer


class CreateOrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    features = CreateOrderFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['owner', 'service', 'provider', 'features', 'order_total']

    def validate(self, data):
        service = data.get('service')
        provider = data.get('provider')

        if service.provider != provider:
            raise serializers.ValidationError('The service does not belong to the specified provider.')

        return data

