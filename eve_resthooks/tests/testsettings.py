MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'user'
MONGO_PASSWORD = 'user'
MONGO_DBNAME = 'testdb'

URL_PREFIX = 'api'
API_VERSION = 'v1'

SERVER_NAME = 'localhost:5000'

books = {
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],
    'schema': {
        'name': {'type': 'string'}
    }
}

DOMAIN= {'books': books}