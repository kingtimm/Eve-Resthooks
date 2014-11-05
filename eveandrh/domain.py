subscriptions = {
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'schema': {
        'event': {
            'nodupesubs': 'true',
            'type': 'string'
        },
        'target_url': {
            'type': 'string'
        }
    }
}

_jobs = {
    'resource_methods': ['GET'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'schema': {
        'target_url': {'type': 'string'},
        'payload': {'type': 'dict'},
        'status': {'type': 'integer'},
        'result': {'type': 'string'},
        'claimed': {'type': 'boolean'},
        'event': {'type': 'string'},
    }
}


DOMAIN = {
    'subscriptions': subscriptions,
    '_jobs': _jobs,
}