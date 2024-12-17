from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.order_models.order import Order
from orders.serializers.create.create_order_item_serializer import CreateOrderItemSerializer

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.order_models.order import Order
from orders.serializers.create.create_order_item_serializer import CreateOrderItemSerializer


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.phone_number')
    items = CreateOrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        try:
            return sum(item.order_item_subtotal for item in obj.items.all())
        except Exception:
            return 0.0

    class Meta:
        model = Order
        fields = ['user', 'items', 'total_price']

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
        try:
            items_data = validated_data.pop('items', [])

            try:
                order = Order.objects.create(**validated_data)
            except Exception:
                raise ValidationError("Failed to create order")

            # Process and create order items
            for item in items_data:
                try:
                    # Prepare item data
                    item_data = {
                        'order': order,
                        'service': item['service'].id,
                        'provider': item['provider'].id,
                    }

                    # Handle features
                    features_data = item.get('features', [])
                    if features_data:
                        item_data['features'] = [
                            {'feature': feature['feature'].id} for feature in features_data
                        ]

                    # Create order item
                    try:
                        item_serializer = CreateOrderItemSerializer(
                            data=item_data,
                            context={'order': order}
                        )
                        item_serializer.is_valid(raise_exception=True)
                        item_serializer.save()
                    except serializers.ValidationError:
                        # Optionally delete the order if item creation fails
                        order.delete()
                        raise ValidationError("Invalid order item data")
                    except Exception:
                        # Optionally delete the order if item creation fails
                        order.delete()
                        raise ValidationError("Failed to create order items")
                except ValidationError:
                    order.delete()
                    raise ValidationError("Failed to create order items")

            return order

        except Exception:
            raise ValidationError("Failed to create order")