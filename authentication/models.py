from django.utils.timezone import now
from django.db import models
import datetime
from user.models import User

class PhoneOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now() > self.created_at + datetime.timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.phone_number} - {self.otp}"


