import json
from eve_resthooks.tests.base import TestMethodsBase


class TestMethodsUpdate(TestMethodsBase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def post_dummy_book_replaced_subscription_with_name_filter(self):
        payload = dict(
            event="books.replaced",
            target_url="http://localhost:6000/dummy",
            filter='{"name":"Testsuite Made up Names by Tim King"}'
        )
        self._post("subscriptions", payload)

    def put_dummy_book(self, original_item, name=None):
        name = name if name is not None else "Testsuite Made up Name 2nd Edition by Tim King"
        payload = dict(
            name=name
        )

        etag, id = original_item['_etag'], original_item['_id']

        return self._put("books", payload, etag, item=id)

    def test_replace_item(self):
        post_response = self.post_dummy_book()
        original_item = json.loads(post_response.data.decode('utf8'))

        put_result = self.put_dummy_book(original_item)

        self.assertEqual(put_result.status_code, 200)

    def test_replace_item_with_sub_name_filter(self):
        post_response = self.post_dummy_book()
        original_item = json.loads(post_response.data.decode('utf8'))

        self.post_dummy_book_replaced_subscription_with_name_filter()

        put_result = self.put_dummy_book(original_item)

        jobs = self.get_jobs()

        self.assertTrue(jobs)