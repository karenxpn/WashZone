from django.contrib.gis.db.models import PointField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from user.models import User
from .category import Category


class Provider(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='providers')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='providers')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    location = PointField()


    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Rating from 0 to 5"
    )

    number_of_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkingHour(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='working_hours')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        unique_together = ('provider', 'weekday')

    def __str__(self):
        return f"{self.get_weekday_display()} ({self.opening_time} - {self.closing_time})"


class SpecialClosure(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='special_closures')
    date = models.DateField()
    reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('provider', 'date')

    def __str__(self):
        return f"{self.date} - {self.reason or 'Closed'}"
