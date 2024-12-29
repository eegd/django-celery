from django.urls import path

from app.views import subscribe, subscribe_ws, task_status, webhook, webhook_async


urlpatterns = [
    path("form/", subscribe, name="form"),
    path('form_ws/', subscribe_ws, name='form_ws'),
    path("task_status/", task_status, name="task_status"),
    path("webhook/", webhook, name="webhook"),
    path('webhook_async/', webhook_async, name='webhook_async'),

]
