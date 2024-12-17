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
        try:
            representation = super().to_representation(instance)

            try:
                items = instance.items.prefetch_related(
                    'order_item_features',
                    'service',
                    'provider'
                ).all()

                representation['items'] = CreateOrderItemSerializer(items, many=True).data
            except Exception:
                representation['items'] = []

            return representation
        except Exception:
            raise ValidationError({"detail": "Failed to represent order data"})

    def create(self, validated_data):
        try:
            # Pop items data to avoid issues with nested creation
            items_data = validated_data.pop('items', [])

            try:
                # Create the main order
                order = Order.objects.create(**validated_data)
            except Exception:
                raise ValidationError({"order": "Failed to create order"})

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
                        raise ValidationError({"items": "Invalid order item data"})
                    except Exception:
                        # Optionally delete the order if item creation fails
                        order.delete()
                        raise ValidationError({"items": "Failed to create order items"})
                except ValidationError:
                    order.delete()
                    raise ValidationError({"items": "Failed to create order items"})

            return order

        except Exception:
            raise ValidationError({"detail": "Failed to create order"})