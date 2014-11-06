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

    def post_dummy_book(self):
        payload = dict(
            name="Testsuite Made up Names by Tim King",
        )
        post_result = self.local_client.post("/api/v1/books", data=json.dumps(payload), headers=self.headers)

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