from rest_framework import serializers

from orders.order_models.order import Order
from orders.order_models.order_item import OrderItem
from orders.order_models.order_item_feature import OrderItemFeature
from services.service_models.feature import ServiceFeature


class CreateOrderItemFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemFeature
        fields = ['feature', 'extra_cost']

    def create(self, validated_data):
        feature = validated_data['feature']
        order_item = validated_data['order_item']

        service_feature = ServiceFeature.objects.filter(
            service=order_item.service,
            feature=feature
        ).first()

        validated_data['extra_cost'] = service_feature.extra_cost if service_feature and not service_feature.is_included else 0
        return super().create(validated_data)



class CreateOrderItemSerializer(serializers.ModelSerializer):
    features = CreateOrderItemFeatureSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ['service', 'provider', 'features']

    def validate(self, data):
        if data['service'].provider != data['provider']:
            raise serializers.ValidationError('The service does not belong to the specified provider.')
        return data

    def create(self, validated_data):
        feature_data = validated_data.pop('features', [])
        order_item = OrderItem.objects.create(**validated_data)

        for feature in feature_data:
            feature_data['order_item'] = order_item
            OrderItemFeature.objects.create(order_item=order_item, **feature)

        return order_item


class CreateOrderSerializer(serializers.ModelSerializer):
    items = CreateOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['user', 'items']


