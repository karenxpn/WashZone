from django.db import models
from orders.order_models.order import Order
from services.service_models.provider import Provider
from services.service_models.service import Service
from services.service_models.feature import Feature


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="order_items")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="order_items")
    features = models.ManyToManyField(Feature, through='OrderItemFeature', blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def order_item_subtotal(self):
        service_price = self.service.base_price
        feature_price = sum(
            feature.extra_cost for feature in self.order_item_features.all()
        )
        return (service_price + feature_price) * self.quantity
