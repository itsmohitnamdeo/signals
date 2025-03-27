from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from signal_app.models import SignalLog
import threading
import time
import uuid

@receiver(post_save, sender=User)
def signal_handler(sender, instance, **kwargs):
    start_time = time.time()
    transaction_id = str(uuid.uuid4())  
    thread_name = threading.current_thread().name  

    # Ensure we log the exact thread where the signal executes
    log, created = SignalLog.objects.get_or_create(user=instance)
    log.is_sync = (thread_name == "MainThread")  # Check if synchronous
    log.thread_name = thread_name
    log.transaction_id = transaction_id
    log.execution_time = round(time.time() - start_time, 4)
    log.save()
