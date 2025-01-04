import random

import requests

from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger

from app.consumers import notify_channel_layer


logger = get_task_logger(__name__)


@shared_task()
def task_call():
    # used for testing a failed api call
    if random.choice([0, 1]):
        raise Exception('random processing error')

    # used for simulating a call to a third-party api
    requests.post('https://httpbin.org/delay/5')


@shared_task(bind=True)
def task_process_notification(self):
    try:
        if not random.choice([0, 1]):
            raise Exception('random processing error')

        # this would block the I/O
        requests.post('https://httpbin.org/delay/5')
    except Exception as e:
        logger.error('exception raised, it would be retry after 5 seconds')
        raise self.retry(exc=e, countdown=5)


@shared_task(name='task_clear_session')
def task_clear_session():
    from django.core.management import call_command
    call_command('clearsessions')


@shared_task(name='default:default_task')
def task_default():
    logger.info('default task is processing')


@shared_task(name='low_priority:low_priority_task')
def task_low_priority():
    logger.info('low priority task is processing')


@shared_task(name='high_priority:high_priority_task')
def task_high_priority():
    logger.info('high priority task is processing')


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    """
    When celery task finish, send notification to Django channel_layer, so Django channel would receive
    the event and then send it to web client
    """
    notify_channel_layer(task_id)
