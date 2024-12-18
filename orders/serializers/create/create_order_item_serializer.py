from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

        try:
            service = Service.objects.select_related('provider').get(pk=service.pk)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Invalid service selected')

        if service.provider != provider:
            raise serializers.ValidationError('The service does not belong to the specified provider.')

        return data

    def create(self, validated_data):
        service = validated_data.get('service')
        provider = validated_data.get('provider')
        order = self.context.get('order')

        if not order:
            raise serializers.ValidationError("Order context is required")

        features_data = validated_data.pop('features', [])

        order_item = OrderItem.objects.create(
            order=order,
            service=service,
            provider=provider
        )

        # Process features
        for feature in features_data:
            feature_data = {
                'feature': feature['feature'].id,
            }

            feature_serializer = CreateOrderItemFeatureSerializer(
                data=feature_data,
                context={'order_item': order_item.id}
            )
            feature_serializer.is_valid(raise_exception=True)
            feature_serializer.save()

        return order_item