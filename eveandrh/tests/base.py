import json
import os
from unittest import TestCase
from eve import Eve
from pymongo import MongoClient
from eveandrh.eveapp import Eveandrh
from eveandrh.tests.testsettings import *
from urllib.parse import urljoin

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


class TestMethodsBase(TestBaseMinimal):
    def setUp(self):
        self.event_created = "books.created"
        self.event_replaced = "books.replaced"
        self.event_updated = "books.updated"
        self.event_deleted = "books.deleted"

        self.target_url = "http://localhost:6000/dummy"

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def _build_url(self, resource, item):
        base = self.apiapp.api_prefix

        if item:
            return "{0}/{1}/{2}".format(base, resource, item)
        else:
            return "{0}/{1}".format(base, resource)

    def _setup_change_operation(self, etag, item, payload, resource):
        url = self._build_url(resource, item)
        headers = {
            "If-Match": etag
        }
        headers.update(self.headers)
        payload = json.dumps(payload)
        return headers, payload, url

    def _post(self, resource, payload, headers=None, item=None):

        if headers:
            self.headers.update(headers)

        url = self._build_url(resource, item)

        payload = json.dumps(payload)
        return self.local_client.post(url, data=payload, headers=self.headers)

    def _get(self, resource, item=None, headers=None):

        url = self._build_url(resource, item)

        return self.local_client.get(url, headers=None)

    def _patch(self, resource, payload, etag, item=None):
        headers, payload, url = self._setup_change_operation(etag, item, payload, resource)

        return self.local_client.patch(url, data=payload, headers=headers)

    def _put(self, resource, payload, etag, item=None):
        headers, payload, url = self._setup_change_operation(etag, item, payload, resource)

        return self.local_client.put(url, data=payload, headers=headers)

    def _delete(self, resource, etag, item):
        payload = {}
        headers, _, url = self._setup_change_operation(etag, item, payload, resource)

        return self.local_client.delete(url, headers=headers)

    def _parse_get_items(self, response):
        return json.loads(response.data.decode('utf8'))['_items']

    def get_jobs(self):
        response = self._get('_jobs')

        return self._parse_get_items(response)

    def get_subscriptions(self):
        response = self._get('subscriptions')

        return self._parse_get_items(response)

    def post_dummy_book(self, name=None):
        name = name if name is not None else "Testsuite Made up Names by Tim King"
        payload = dict(
            name=name,
        )

        return self._post("books", payload)

    def post_dummy_book_created_subscription(self):
        payload = dict(
            event="books.created",
            target_url="http://localhost:6000/dummy",
        )
        return self._post("subscriptions", payload)
