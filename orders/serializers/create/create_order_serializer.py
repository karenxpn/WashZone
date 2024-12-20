from rest_framework import serializers
from orders.order_models.order import Order
from orders.order_models.order_feature import OrderFeature
from orders.order_models.time_slot import TimeSlot
from orders.serializers.create.create_order_feature_serializer import CreateOrderFeatureSerializer
from orders.serializers.validate_time_slot import validate_time_slot
from services.service_models.feature import ServiceFeature


class CreateOrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    features = CreateOrderFeatureSerializer(many=True, write_only=True)
    start_time = serializers.DateTimeField(write_only=True)
    end_time = serializers.DateTimeField(write_only=True)


    class Meta:
        model = Order
        fields = ['owner', 'service', 'provider', 'features', 'order_total', 'order_duration', 'start_time', 'end_time']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        return representation


    def validate(self, data):
        service = data.get('service')
        provider = data.get('provider')

        if service.provider != provider:
            raise serializers.ValidationError('The service does not belong to the specified provider.')

        validate_time_slot(provider, service, data)

        return data


    def create(self, validated_data):
        features_data = validated_data.pop('features', [])
        service = validated_data.get('service')
        start_time = validated_data.pop('start_time')
        end_time = validated_data.pop('end_time')

        time_slot = TimeSlot.objects.create(provider=validated_data['provider'], start_time=start_time, end_time=end_time, is_available=False)

        order = Order.objects.create(
            **validated_data,
            service_name=service.name,
            service_description=service.description,
            service_price=service.base_price,
            service_duration=service.duration_in_minutes,
            time_slot=time_slot
        )
        service = order.service

        order_features = []
        for feature_data in features_data:
            feature = feature_data['feature']

            service_feature = ServiceFeature.objects.get(
                service=service,
                feature=feature.id
            )

            extra_cost = (
                service_feature.extra_cost
                if service_feature and not service_feature.is_included
                else 0
            )

            extra_duration =(
                service_feature.extra_time_in_minutes
                if service_feature and not service_feature.is_included
                else 0
            )

            order_features.append(OrderFeature(order=order,
                                               feature=feature,
                                               feature_name=feature.name,
                                               feature_description=feature.description,
                                               extra_cost=extra_cost,
                                               extra_duration=extra_duration))

        OrderFeature.objects.bulk_create(order_features)

        return order

