from django.db import models
from orders.order_models.order import Order
from services.service_models.service import Service
from services.service_models.feature import Feature


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    features = models.ManyToManyField(Feature, through='OrderItemFeature', blank=True)

    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_total_price(self):
        service_price = self.service.base_price
        feature_price = sum(
            feature.extra_cost for feature in self.order_item_features.all()
        )
        return (service_price + feature_price) * self.quantity

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
