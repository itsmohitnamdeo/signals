from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import transaction
from signal_app.models import SignalLog
from signal_app.rectangle import Rectangle
import threading

# View 1: Test Synchronous Signal
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

# View 2: Test Signal in a Transaction
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
        "log_exists_after_rollback": log_exists,
    })

# View 3: Test Signals Running in Different Threads
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

# View 4: Test Rectangle Class
def test_rectangle(request):
    try:
        length = int(request.GET.get('length', 10))
        width = int(request.GET.get('width', 5))
        rect = Rectangle(length, width)
        data = {
            "iterable_values": [item for item in rect],
            "area": rect.area(),
            "perimeter": rect.perimeter(),
        }
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse(data)
