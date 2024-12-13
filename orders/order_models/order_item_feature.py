from django.db import models

from orders.order_models.order_item import OrderItem
from services.service_models.feature import Feature


class OrderItemFeature(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="order_item_features")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    extra_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.feature.name} (Extra Cost: {self.extra_cost})"
