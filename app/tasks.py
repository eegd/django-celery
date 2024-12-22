import random

import requests

from celery import shared_task
from celery.utils.log import get_task_logger

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
