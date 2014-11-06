import json
from eveandrh.tests.base import TestBaseMinimal


class TestSubscriptions(TestBaseMinimal):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def post_dummy_book_created_subscription(self):
        payload = dict(
            event="books.created",
            target_url="http://localhost:6000/dummy",
        )
        return self.local_client.post("/api/v1/subscriptions", data=json.dumps(payload), headers=self.headers)

    def post_dummy_book_updated_subscription_without_filter(self):
        payload = dict(
            event="books.updated",
            target_url="http://localhost:6000/dummy",
        )
        return self.local_client.post("/api/v1/subscriptions", data=json.dumps(payload), headers=self.headers)

    def post_dummy_book_updated_subscription_with_name_filter(self):
        payload = dict(
            event="books.updated",
            target_url="http://localhost:6000/dummy",
            filter='{"name":"Testsuite Made up Names by Tim King"}'
        )
        return self.local_client.post("/api/v1/subscriptions", data=json.dumps(payload), headers=self.headers)

    def post_dummy_book_updated_subscription_with_id_filter(self, id):
        payload = dict(
            event="books.updated",
            target_url="http://localhost:6000/dummy",
            filter='{{"_id":"{0}"}}'.format(id)
        )
        return self.local_client.post("/api/v1/subscriptions", data=json.dumps(payload), headers=self.headers)

    def post_dummy_book(self, name=None):
        name = name if name is not None else "Testsuite Made up Names by Tim King"
        payload = dict(
            name=name,
        )

        return self.local_client.post("/api/v1/books", data=json.dumps(payload), headers=self.headers)

    def patch_dummy_book(self, original_item, name=None):
        name = name if name is not None else "Testsuite Made up Name 2nd Edition by Tim King"
        payload = dict(
            name=name
        )

        headers = {
            "If-Match": original_item['_etag']
        }

        headers.update(self.headers)

        url = "/api/v1/books/{_id}".format(**original_item)

        return self.local_client.patch(url, data=json.dumps(payload), headers=headers)

    def get_jobs(self):
        return json.loads(self.local_client.get("/api/v1/_jobs").data.decode('utf8'))['_items']

    def get_subscriptions(self):
        return json.loads(self.local_client.get("/api/v1/subscriptions").data.decode('utf8'))['_items']

    def test_add_subscription_creates(self):
        sub_result = self.post_dummy_book_created_subscription()

        self.assertEqual(sub_result.status_code, 201)

    def test_no_subscriptions_no_jobs(self):
        self.post_dummy_book()

        jobs = self.get_jobs()

        self.assertFalse(jobs)

    def test_add_subscription_adds_job(self):
        sub_result = self.post_dummy_book_created_subscription()

        self.post_dummy_book()

        jobs = self.get_jobs()

        self.assertTrue(jobs)

    def test_add_subscription_same_target_does_not_duplicate(self):
        sub1 = self.post_dummy_book_created_subscription()

        sub2 = self.post_dummy_book_created_subscription()

        subscriptions = self.get_subscriptions()

        self.assertEqual(len(subscriptions), 1)

    def test_add_subscription_different_target_makes_two_jobs(self):
        sub1 = self.post_dummy_book_created_subscription()

        payload = dict(
            event="books.created",
            target_url="http://remotehost:6000/dummy",
        )

        sub2 = self.local_client.post("/api/v1/subscriptions", data=json.dumps(payload), headers=self.headers)

        subscriptions = self.get_subscriptions()

        self.assertEqual(len(subscriptions), 2)

    def test_add_subscription_different_event_makes_two_jobs(self):
        sub1 = self.post_dummy_book_created_subscription()

        payload = dict(
            event="books.updated",
            target_url="http://localhost:6000/dummy",
        )

        sub2 = self.local_client.post("/api/v1/subscriptions", data=json.dumps(payload), headers=self.headers)

        subscriptions = self.get_subscriptions()

        self.assertEqual(len(subscriptions), 2)

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