import random

from string import ascii_lowercase


def route_task(name, args, kwargs, options, task=None, **kw):
    if ':' in name:
        queue, _ = name.split(':')
        return {'queue': queue}
    return {'queue': 'default'}


def random_username():
    username = ''.join([random.choice(ascii_lowercase) for i in range(5)])
    return username
