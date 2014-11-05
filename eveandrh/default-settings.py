# will need to add db user: db.addUser( { user: "user", pwd: "password", roles: [ "readWrite" ] } )

from eveandrh.domain import DOMAIN


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'user'
MONGO_PASSWORD = 'password'
MONGO_DBNAME = 'api'

URL_PREFIX = 'api'
API_VERSION = 'v1'

SERVER_NAME = 'localhost:5000'