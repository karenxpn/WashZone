from django.db import models

from user.models import User
from .provider import Provider


class Service(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="services")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_services")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_in_minutes = models.PositiveIntegerField()  # Estimated duration of service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.provider.name})"
