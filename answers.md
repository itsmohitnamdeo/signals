
### Question 1: By default, are Django signals executed synchronously or asynchronously?

Answer: By default, Django signals are executed synchronously. This means that when an event occurs (like saving a model instance), the registered signal handlers execute in the same thread before the execution moves forward.

We can confirm this with the following code snippet:

Code: Testing if Django signals execute synchronously

models.py

```
from django.db import models
from django.contrib.auth.models import User
import uuid

class SignalLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_sync = models.BooleanField(default=True)  
    thread_name = models.CharField(max_length=100, default="Unknown")
    transaction_id = models.UUIDField(default=uuid.uuid4)
    execution_time = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.thread_name}"
```

signals.py
```
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

    log, created = SignalLog.objects.get_or_create(user=instance)
    log.is_sync = (thread_name == "MainThread")  # Check if executed synchronously
    log.thread_name = thread_name
    log.transaction_id = transaction_id
    log.execution_time = round(time.time() - start_time, 4)
    log.save()
```

views.py
  ```
  from django.http import JsonResponse
  from django.contrib.auth.models import User
  from signal_app.models import SignalLog
  
  def test_sync_signal(request):
      user, created = User.objects.get_or_create(username="sync_user")
      log, _ = SignalLog.objects.get_or_create(user=user)
  
      return JsonResponse({
          "message": "User created, signal executed",
          "username": user.username,
          "is_sync": log.is_sync,
          "thread_name": log.thread_name,
          "transaction_id": log.transaction_id,
          "execution_time": log.execution_time
      })
   ```
- Output

  ![test-sync](https://github.com/user-attachments/assets/88ca5a01-c392-4127-b8cc-755e741dac86)

- Conclusion

The is_sync flag confirms that the signal executes in the same thread, meaning Django signals are synchronous by default.

### Question 2: Do Django signals run in the same thread as the caller?

Answer: Yes, by default, Django signals run in the same thread as the caller. This means that if a model instance is saved in a thread, the signal executes in the same thread.

To verify this, let's test signal execution in multiple threads.

Code: Testing if Django signals run in the same database transaction as the caller

Viwes.py
```
import threading
from django.http import JsonResponse
from django.contrib.auth.models import User
from signal_app.models import SignalLog

def test_thread_signal(request):
    def create_user(thread_name):
        user, created = User.objects.get_or_create(username=f"thread_user_{thread_name}")
        log, _ = SignalLog.objects.get_or_create(user=user)
        return {
            "username": user.username,
            "thread_name": log.thread_name
        }

    thread1 = threading.Thread(target=create_user, args=("TestThread-1",))
    thread2 = threading.Thread(target=create_user, args=("TestThread-2",))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    return JsonResponse({
        "message": "Threads executed with signals",
        "thread1_result": create_user("TestThread-1"),
        "thread2_result": create_user("TestThread-2")
    })
```

- Output

![test-thread](https://github.com/user-attachments/assets/c8daff42-f524-41fb-b090-0917f138d9f1)


- Conclusion

The signals executed in Thread-2 and Thread-3, confirming that Django signals run in the same thread as the caller by default.

### Question 3: By default, do Django signals run in the same database transaction as the caller?

Answer: By default, Django signals do not run in the same database transaction as the caller. If a database transaction is rolled back, the signal execution is not automatically reverted.

We can test this by creating a user inside an atomic transaction and then forcing a rollback.

Code: Testing if Django signals run in the same database transaction as the caller
views.py
```
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.models import User
from signal_app.models import SignalLog

def test_transaction_signal(request):
    try:
        with transaction.atomic():
            user, created = User.objects.get_or_create(username="transaction_user")
            raise Exception("Forcing rollback")  # This will roll back the transaction
    except Exception:
        pass

    log_exists = SignalLog.objects.filter(user__username="transaction_user").exists()

    return JsonResponse({
        "message": "User created inside transaction",
        "log_exists_after_rollback": log_exists
    })
```

- Output

  ![test-transaction](https://github.com/user-attachments/assets/bab16daf-4809-4208-bc06-0ff80a811aa5)


- Conclusion

  Even though the transaction was rolled back, the SignalLog entry still exists, proving that Django signals run outside of the caller's database transaction by default.


### Final Summary:

- Are Django signals synchronous by default?	✅ Yes	Signals execute in the same execution flow as the caller.
- Do Django signals run in the same thread as the caller?	✅ Yes	Signals execute in the same thread where the caller executes.
- Do Django signals run in the same database transaction as the caller?	❌ No	Signal actions persist even if the caller's transaction is rolled back.

### Implementation of Rectangle Class

```
class Rectangle:
    def __init__(self, length: int, width: int):
        if not isinstance(length, int) or not isinstance(width, int):
            raise ValueError("Both length and width must be integers")
        if length <= 0 or width <= 0:
            raise ValueError("Length and width must be positive integers")
        self.length = length
        self.width = width
        self._index = 0

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == 0:
            self._index += 1
            return {'length': self.length}
        elif self._index == 1:
            self._index += 1
            return {'width': self.width}
        else:
            raise StopIteration

    def area(self):
        """Calculate area of rectangle."""
        return self.length * self.width

    def perimeter(self):
        """Calculate perimeter of rectangle."""
        return 2 * (self.length + self.width)
```

- Output

![test-rectangle](https://github.com/user-attachments/assets/85a176be-b212-4020-8a98-74de034ee987)

