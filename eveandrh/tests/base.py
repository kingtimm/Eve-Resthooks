import os
from unittest import TestCase
from eve import Eve
from pymongo import MongoClient
from eveandrh.eveapp import Eveandrh
from eveandrh.tests.testsettings import *


class TestBaseMinimal(TestCase):
    def setUp(self):
        settings_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'testsettings.py')

        self.headers = {'Content-Type': 'application/json'}

        self.setupDB()

        self.apiapp = Eve(settings=settings_path)
        self.eveandrh = Eveandrh(self.apiapp)

        self.local_client = self.apiapp.test_client()

    def setupDB(self):
        self.connection = MongoClient(MONGO_HOST, MONGO_PORT)
        self.connection.drop_database(MONGO_DBNAME)
        if MONGO_USERNAME:
            self.connection[MONGO_DBNAME].add_user(MONGO_USERNAME,
                                                   MONGO_PASSWORD)

    def bulk_insert(self):
        pass

    def dropDB(self):
        self.connection = MongoClient(MONGO_HOST, MONGO_PORT)
        self.connection.drop_database(MONGO_DBNAME)
        self.connection.close()

