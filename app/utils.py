def route_task(name, args, kwargs, options, task=None, **kw):
    if ':' in name:
        queue, _ = name.split(':')
        return {'queue': queue}
    return {'queue': 'default'}
