import json
from eve_resthooks.tests.base import TestMethodsBase


class TestMethodsDelete(TestMethodsBase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def post_dummy_book_deleted_subscription_with_name_filter(self):
        payload = dict(
            event="books.deleted",
            target_url="http://localhost:6000/dummy",
            filter='{"name":"Testsuite Made up Names by Tim King"}'
        )
        self._post("subscriptions", payload)

    def delete_dummy_book(self, original_item):
        etag, id = original_item['_etag'], original_item['_id']

        return self._delete("books",  etag, item=id)

    def test_delete_item(self):
        post_response = self.post_dummy_book()
        original_item = json.loads(post_response.data.decode('utf8'))

        delete_result = self.delete_dummy_book(original_item)

        self.assertEqual(delete_result.status_code, 200)

    def test_delete_item_with_sub_name_filter(self):
        post_response = self.post_dummy_book()
        original_item = json.loads(post_response.data.decode('utf8'))

        self.post_dummy_book_deleted_subscription_with_name_filter()

        delete_result = self.delete_dummy_book(original_item)

        jobs = self.get_jobs()

        self.assertTrue(jobs)