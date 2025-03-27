from django.db import models
from django.contrib.auth.models import User
import uuid

class SignalLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_sync = models.BooleanField(default=True) 
    thread_name = models.CharField(max_length=100, default='Unknown')
    transaction_id = models.UUIDField(default=uuid.uuid4)
    execution_time = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.thread_name}"
