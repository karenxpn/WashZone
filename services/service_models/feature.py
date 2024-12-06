# features that the service includes or can be added
from django.db import models

from services.service_models.service import Service


class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# intermediate model for the feature and service ( many-to-many relationship)

class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='services')
    is_included = models.BooleanField(default=False)
    extra_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Extra cost for the feature if it's optional"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('service', 'feature')

    def __str__(self):
        return f"{self.service.name} - {self.feature.name}"