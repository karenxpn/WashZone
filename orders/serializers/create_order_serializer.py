from rest_framework import serializers

from orders.order_models.order import Order
from orders.order_models.order_item import OrderItem
from orders.order_models.order_item_feature import OrderItemFeature
from services.serializers.provider_serializer import ProviderSerializer
from services.serializers.service_serializer import ServiceSerializer
from services.service_models.feature import ServiceFeature, Feature
from services.service_models.provider import Provider
from services.service_models.service import Service


class CreateOrderItemFeatureSerializer(serializers.ModelSerializer):
    feature = serializers.PrimaryKeyRelatedField(queryset=Feature.objects.all(), write_only=True)

    class Meta:
        model = OrderItemFeature
        fields = ['feature', 'extra_cost']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['feature_id'] = instance.id
        representation['feature_name'] = instance.name
        representation['feature_description'] = instance.description

        return representation


    def create(self, validated_data):
        feature = validated_data['feature']
        order_item_pk = self.context.get('order_item')

        service = OrderItem.objects.get(pk=order_item_pk).service.id

        service_feature = ServiceFeature.objects.filter(
            service=service,
            feature=feature.id,
        ).first()

        validated_data['extra_cost'] = service_feature.extra_cost if service_feature and not service_feature.is_included else 0

        order_item = OrderItem.objects.get(pk=order_item_pk)

        order_item_feature = OrderItemFeature.objects.create(
            order_item=order_item,
            feature=feature,
            extra_cost=validated_data['extra_cost'],
        )

        return order_item_feature



class CreateOrderItemSerializer(serializers.ModelSerializer):
    features = CreateOrderItemFeatureSerializer(many=True, required=False)
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), write_only=True)
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all(), write_only=True)


    class Meta:
        model = OrderItem
        fields = ['service', 'provider', 'features']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Include related features via the reverse relationship
        representation['features'] = CreateOrderItemFeatureSerializer(
            instance.features.all(), many=True
        ).data

        representation['service_id'] = instance.service.id
        representation['service_name'] = instance.service.name
        representation['provider'] = ProviderSerializer(instance.provider).data
        return representation

    def validate(self, data):
        service = data.get('service')
        provider = data.get('provider')

        if not Service.objects.filter(pk=service.pk, provider_id=provider.id).exists():
            raise serializers.ValidationError('The service does not belong to the specified provider.')

        return data

    def create(self, validated_data):
        service = validated_data.get('service')
        provider = validated_data.get('provider')
        order = self.context.get('order')

        features_data = validated_data.pop('features', [])

        order_item = OrderItem.objects.create(
            order=order,
            service=service,
            provider=provider,
        )


        for feature in features_data:
            feature_data = {
                'feature': feature['feature'].id,
            }

            item_serializer = CreateOrderItemFeatureSerializer(
                data=feature_data,
                context={'order_item': order_item.id}
            )

            item_serializer.is_valid(raise_exception=True)
            item_serializer.save()

        return order_item


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.phone_number')
    items = CreateOrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return sum(item.order_item_subtotal for item in obj.items.all())

    class Meta:
        model = Order
        fields = ['user', 'items', 'total_price']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = CreateOrderItemSerializer(instance.items.all(), many=True).data
        return representation


    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)

        for item in items_data:
            item_data = {
                'service': item['service'].id,
                'provider': item['provider'].id,
            }

            features_data = item.get('features', [])
            item_data['features'] = [
                {'feature': feature['feature'].id for feature in features_data},
            ]

            item_serializer = CreateOrderItemSerializer(
                data=item_data,
                context={'order': order}
            )

            item_serializer.is_valid(raise_exception=True)
            item_serializer.save()

        return order

