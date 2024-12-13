from django.db import models
from services.service_models.provider import Provider


class Order(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="orders")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ], default='pending')

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        return sum(item.total_price for item in self.items.all())

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Reservation {self.id} by {self.user.username}'