import random
import time

import requests

from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from functools import partial

from app.forms import Form
from app.tasks import task_call, task_send_email, task_process_notification
from app.utils import random_username

logger = get_task_logger(__name__)


def subscribe(request) -> HttpResponse:
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            task = task_call.delay()  # type: ignore
            # return the task id so the JS can poll the state
            return JsonResponse({'task_id': task.task_id})

    form = Form()
    return render(request, 'form.html', {'form': form})


def subscribe_ws(request):
    """
    Use Websocket to get notification of Celery task, instead of using ajax polling
    """
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            task = task_call.delay()  # type: ignore
            # return the task id so the JS can poll the state
            return JsonResponse({
                'task_id': task.task_id,
            })

    form = Form()
    return render(request, 'form_ws.html', {'form': form})


def task_status(request) -> JsonResponse:
    task_id = request.GET.get('task_id')

    if task_id:
        task = AsyncResult(task_id)
        state = task.state

        if state == 'FAILURE':
            error = str(task.result)
            response = {
                'state': state,
                'error': error,
            }
        else:
            response = {
                'state': state,
            }
        return JsonResponse(response)

    return JsonResponse({
        'state': 'FAILURE',
        'error': 'task id not existed',
    })


@csrf_exempt
def webhook(request) -> HttpResponse:
    if not random.choice([0, 1]):
        raise Exception('random processing error')

    requests.post('https://httpbin.org/delay/5')
    return HttpResponse('pong')


@csrf_exempt
def webhook_async(request) -> HttpResponse:
    task = task_process_notification.delay()  # type: ignore
    logger.info(f"Task ID: {task.id}")
    return HttpResponse('pong')


@transaction.atomic
def transaction_celery(request):
    username = random_username()
    user = User.objects.create_user(username, 'user@mail.com', 'password')
    logger.info(f'create user {user.pk}')
    # the task does not get called until after the transaction is committed
    transaction.on_commit(partial(task_send_email.delay, user.pk))  # type: ignore

    time.sleep(1)
    return HttpResponse('test')
