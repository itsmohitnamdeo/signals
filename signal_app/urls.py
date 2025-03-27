from django.urls import path
from .views import test_sync_signal, test_thread_signal, test_transaction_signal, test_rectangle

urlpatterns = [
    path('test-sync/', test_sync_signal, name='test_sync'),
    path('test-thread/', test_thread_signal, name='test_thread'),
    path('test-transaction/', test_transaction_signal, name='test_transaction'),
    path('test-rectangle/', test_rectangle, name='test_rectangle'),
]
