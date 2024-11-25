from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class PhoneOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now() > self.created_at + datetime.timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.phone_number} - {self.otp}"


