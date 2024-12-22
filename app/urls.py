from django.urls import path

from app.views import subscribe, task_status, webhook, webhook_async


urlpatterns = [
    path("form/", subscribe, name="form"),
    path("task_status/", task_status, name="task_status"),
    path("webhook/", webhook, name="webhook"),
    path('webhook_async/', webhook_async, name='webhook_async'),
]
