from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db.models import PointField
from django.db import models

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    email_promotions_enabled = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=False)
    location = PointField(null=True, blank=True)
    image = models.ImageField(upload_to='users/', null=True, blank=True)

    def __str__(self):
        return self.username

