# services that the provider offers
from django.db import models
from .provider import Provider


class Service(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=100)  # e.g., "Car Wash", "Detailing", "Ceramic Coating"
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration_in_minutes = models.PositiveIntegerField(blank=True, null=True)  # Estimated duration of service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.provider.name})"
