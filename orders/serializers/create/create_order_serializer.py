from rest_framework import serializers

from orders.order_models.order import Order
from orders.serializers.create.create_order_item_serializer import CreateOrderItemSerializer


class CreateOrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    items = CreateOrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return sum(item.order_item_subtotal for item in obj.items.all())

    class Meta:
        model = Order
        fields = ['owner', 'items', 'total_price']


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        items = instance.items.prefetch_related(
            'order_item_features',
            'service',
            'provider'
        ).all()

        representation['items'] = CreateOrderItemSerializer(items, many=True).data
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
            if features_data:
                item_data['features'] = [
                    {'feature': feature['feature'].id for feature in features_data},
                ]

            item_serializer = CreateOrderItemSerializer(
                data=item_data,
                context={'order': order}
            )

            item_serializer.is_valid(raise_exception=False)
            item_serializer.save()

        return order

