from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .category import Category


class Provider(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='providers')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

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