import logging
import os
from eveandrh.eveapp import Eveandrh

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')


def build_wsgi_application(settings_path):
    app = Eveandrh(settings=settings_path, static_folder=None)
    app.local_client = app.test_client()

    return app


if __name__ == '__main__':
    settings = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.py')

    apiapp = build_wsgi_application(settings_path=settings)
    apiapp.debug = True
    apiapp.run()
