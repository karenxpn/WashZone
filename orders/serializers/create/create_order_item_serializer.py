from rest_framework import serializers

from orders.order_models.order_item import OrderItem
from orders.serializers.create.create_order_item_feature_serializer import CreateOrderItemFeatureSerializer
from services.serializers.provider_serializer import ProviderSerializer
from services.service_models.provider import Provider
from services.service_models.service import Service


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
            instance.order_item_features.all(), many=True
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
