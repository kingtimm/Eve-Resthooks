import json
from eve_resthooks.tests.base import TestMethodsBase


class TestMethodsUpdate(TestMethodsBase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def post_dummy_book_updated_subscription_without_filter(self):
        payload = dict(
            event="books.updated",
            target_url="http://localhost:6000/dummy",
        )
        return self._post("subscriptions", payload)

    def post_dummy_book_updated_subscription_with_name_filter(self):
        payload = dict(
            event="books.updated",
            target_url="http://localhost:6000/dummy",
            filter='{"name":"Testsuite Made up Names by Tim King"}'
        )
        return self._post("subscriptions", payload)

    def post_dummy_book_updated_subscription_with_id_filter(self, id):
        payload = dict(
            event="books.updated",
            target_url="http://localhost:6000/dummy",
            filter='{{"_id":"{0}"}}'.format(id)
        )
        return self._post("subscriptions", payload)

    def patch_dummy_book(self, original_item, name=None):
        name = name if name is not None else "Testsuite Made up Name 2nd Edition by Tim King"
        payload = dict(
            name=name
        )

        etag, id = original_item['_etag'], original_item['_id']

        return self._patch("books", payload, etag, item=id)

    def test_patch_item_no_subs(self):

        post_response = self.post_dummy_book()
        original_item = json.loads(post_response.data.decode('utf8'))

        patch_result = self.patch_dummy_book(original_item)

        self.assertEqual(patch_result.status_code, 200)

    def test_patch_item_with_sub(self):
        post_response = self.post_dummy_book()
        original_item = json.loads(post_response.data.decode('utf8'))

        post_sub_result = self.post_dummy_book_updated_subscription_without_filter()

        self.patch_dummy_book(original_item)

        jobs = self.get_jobs()

        self.assertTrue(jobs)

    def test_patch_item_with_sub_name_filter(self):
        post_response = self.post_dummy_book()
        original_item = json.loads(post_response.data.decode('utf8'))

        post_sub_result = self.post_dummy_book_updated_subscription_with_name_filter()

        self.patch_dummy_book(original_item)

        jobs = self.get_jobs()

        self.assertTrue(jobs)

    def test_patch_item_with_sub_id_filter(self):
        post_response = self.post_dummy_book()
        original_item = json.loads(post_response.data.decode('utf8'))

        post_sub_result = self.post_dummy_book_updated_subscription_with_id_filter(original_item['_id'])

        self.patch_dummy_book(original_item)

        jobs = self.get_jobs()

        self.assertTrue(jobs)

    def test_patch_item_wrong_name_filter(self):
        post2_response = self.post_dummy_book("The Bogus Chronicles")
        original_item2 = json.loads(post2_response.data.decode('utf8'))

        self.post_dummy_book_updated_subscription_with_name_filter()

        self.patch_dummy_book(original_item2)

        jobs = self.get_jobs()

        self.assertFalse(jobs)