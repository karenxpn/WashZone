from datetime import timedelta

from django.db import models
from services.service_models.provider import Provider


class TimeSlot(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    def is_available_for_duration(self, duration_minutes):
        return self.is_available and (self.end_time - self.start_time >= timedelta(minutes=duration_minutes))

    def reserve_slot(self):
        self.is_available = False
        self.save()

    def __str__(self):
        return f"{self.provider.name} - {self.start_time} to {self.end_time}"

