import json
from eve_resthooks.tests.base import TestMethodsBase


class TestMethodsCreate(TestMethodsBase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_add_subscription_creates(self):
        sub_result = self.post_dummy_book_created_subscription()

        self.assertEqual(sub_result.status_code, 201)

    def test_no_subscriptions_no_jobs(self):
        self.post_dummy_book()

        jobs = self.get_jobs()

        self.assertFalse(jobs)

    def test_add_subscription_adds_job(self):
        sub_result = self.post_dummy_book_created_subscription()

        post_result = self.post_dummy_book()

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

        sub2 = self._post("subscriptions", payload)

        subscriptions = self.get_subscriptions()

        self.assertEqual(len(subscriptions), 2)

    def test_add_subscription_different_event_makes_two_jobs(self):
        sub1 = self.post_dummy_book_created_subscription()

        payload = dict(
            event="books.updated",
            target_url="http://localhost:6000/dummy",
        )

        sub2 = self._post("subscriptions", payload)

        subscriptions = self.get_subscriptions()

        self.assertEqual(len(subscriptions), 2)