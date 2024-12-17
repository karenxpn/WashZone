from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.order_models.order_item import OrderItem
from orders.order_models.order_item_feature import OrderItemFeature
from services.service_models.feature import Feature, ServiceFeature


class CreateOrderItemFeatureSerializer(serializers.ModelSerializer):
    feature = serializers.PrimaryKeyRelatedField(queryset=Feature.objects.all(), write_only=True)

    class Meta:
        model = OrderItemFeature
        fields = ['feature', 'extra_cost']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if isinstance(instance, OrderItemFeature):
            # Adding feature details directly to representation
            representation['feature_id'] = instance.feature.id
            representation['feature_name'] = instance.feature.name
            representation['feature_description'] = instance.feature.description
            representation['extra_cost'] = instance.extra_cost

        return representation

    def create(self, validated_data):
        try:
            feature = validated_data['feature']
            order_item_pk = self.context.get('order_item')

            try:
                order_item = OrderItem.objects.select_related('service').get(pk=order_item_pk)
                service = order_item.service
            except ObjectDoesNotExist:
                raise ValidationError("Invalid order item")

            try:
                # Find service feature
                service_feature = ServiceFeature.objects.filter(
                    service=service,
                    feature=feature.id,
                ).first()

                # Calculate extra cost
                validated_data['extra_cost'] = (
                    service_feature.extra_cost
                    if service_feature and not service_feature.is_included
                    else 0
                )
            except Exception:
                validated_data['extra_cost'] = 0

            try:
                # Create order item feature
                order_item_feature = OrderItemFeature.objects.create(
                    order_item=order_item,
                    feature=feature,
                    extra_cost=validated_data['extra_cost'],
                )
            except Exception:
                raise ValidationError("Failed to create order item feature")

            return order_item_feature

        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Failed to create order item feature")