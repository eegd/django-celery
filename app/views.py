import random

import requests

from celery.result import AsyncResult
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from app.forms import Form
from app.tasks import email_task


def api_call() -> None:
    # used for testing a failed api call
    if random.choice([0, 1]):
        raise Exception('random processing error')

    # used for simulating a call to a third-party api
    requests.post('https://httpbin.org/delay/5')


def subscribe(request) -> HttpResponse:
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            task = email_task.delay()  # type: ignore
            # return the task id so the JS can poll the state
            return JsonResponse({'task_id': task.task_id, })

    form = Form()
    return render(request, 'form.html', {'form': form})


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
        'error': 'task id not found',
    })
