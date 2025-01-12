from django.urls import path

from app.views import subscribe, subscribe_ws, task_status, transaction_celery, webhook, webhook_async


urlpatterns = [
    path("form/", subscribe, name="form"),
    path('form_ws/', subscribe_ws, name='form_ws'),
    path("task_status/", task_status, name="task_status"),
    path("webhook/", webhook, name="webhook"),
    path('webhook_async/', webhook_async, name='webhook_async'),
    path('transaction_celery/', transaction_celery, name='transaction_celery'),
]
