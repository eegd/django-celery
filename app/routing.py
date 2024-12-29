from django.urls import path

from app import consumers


urlpatterns = [
    path('ws/task_status/<task_id>/', consumers.TaskStatusConsumer.as_asgi()),
]
