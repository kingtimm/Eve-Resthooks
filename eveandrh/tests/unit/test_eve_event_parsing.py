import unittest
from eveandrh.controllers import subscriptions


class TestEveEventParsing(unittest.TestCase):

    def test_created(self):
        event_string = "endpoint.created"
        result = subscriptions.get_eve_event_name(event_string)

        self.assertEqual(result, ("endpoint", "inserted"))

    def test_replaced(self):
        event_string = "endpoint.replaced"
        result = subscriptions.get_eve_event_name(event_string)

        self.assertEqual(result, ("endpoint", "replaced"))

    def test_updated(self):
        event_string = "endpoint.updated"
        result = subscriptions.get_eve_event_name(event_string)

        self.assertEqual(result, ("endpoint", "updated"))

    def test_deleted(self):
        event_string = "endpoint.deleted"
        result = subscriptions.get_eve_event_name(event_string)

        self.assertEqual(result, ("endpoint", "deleted"))