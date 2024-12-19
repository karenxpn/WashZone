from django.db import models

from orders.order_models.time_slot import TimeSlot
from services.service_models.feature import Feature
from services.service_models.provider import Provider
from services.service_models.service import Service
from user.models import User


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="orders")

    #### snapshots of the service
    service_name = models.CharField(max_length=255, null=True, blank=True)
    service_description = models.CharField(max_length=255, null=True, blank=True)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_duration = models.DecimalField(max_digits=10, decimal_places=2)
    ####


    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="orders")
    features = models.ManyToManyField(Feature, through='OrderFeature', blank=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True, blank=True)


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
        feature_price = sum(feature.extra_cost for feature in self.order_features.all())
        return self.service_price + feature_price

    @property
    def order_duration(self):
        features_duration = sum(feature.extra_duration for feature in self.order_features.all())
        return self.service_duration + features_duration

    def __str__(self):
        return f'Reservation {self.id} by {self.owner.username}'