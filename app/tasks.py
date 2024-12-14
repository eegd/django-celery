from celery import shared_task

from app.views import api_call


@shared_task()
def email_task():
    api_call()
