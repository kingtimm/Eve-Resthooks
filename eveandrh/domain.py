subscriptions = {
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'schema': {
        'event': {
            'nodupesubs': 'true',
            'type': 'string',
            'required': True,
        },
        'target_url': {
            'type': 'string',
            'required': True
        },
        'filter': {
            'type': 'string',
        }
    }
}

_jobs = {
    'resource_methods': ['GET'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'schema': {
        'target_url': {
            'type': 'string',
            'required': True
        },
        'payload': {
            'type': 'dict',
            'required': True
        },
        'status': {
            'type': 'integer',
            'required': True
        },
        'result': {
            'type': 'string',
            'required': True
        },
        'claimed': {
            'type': 'boolean',
            'required': True
        },
        'event': {
            'type': 'string',
            'required': True},
    }
}


DOMAIN = {
    'subscriptions': subscriptions,
    '_jobs': _jobs,
}