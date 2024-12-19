from django.db import models
from services.service_models.feature import Feature
from services.service_models.provider import Provider
from services.service_models.service import Service
from user.models import User


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="orders")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="orders")
    features = models.ManyToManyField(Feature, through='OrderFeature', blank=True)

    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ], default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def order_total(self):
        service_price = self.service.base_price
        feature_price = sum(feature.extra_cost for feature in self.order_features.all())

        return service_price + feature_price

    @property
    def order_duration(self):
        service_duration = self.service.duration_in_minutes
        features_duration = sum(feature.extra_duration for feature in self.order_features.all())

        return service_duration + features_duration

    def __str__(self):
        return f'Reservation {self.id} by {self.owner.username}'