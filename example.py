import logging
import os
from eve import Eve
from eveandrh.eveapp import Eveandrh

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

if __name__ == '__main__':
    settings = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.py')

    apiapp = Eve(settings=settings)
    eveandrh = Eveandrh(apiapp)
    apiapp.debug = True
    apiapp.run()
