from eve_resthooks.tests.base import TestMethodsBase
from eve.tests.utils import DummyEvent
from eve_resthooks.tests.testsettings import MONGO_DBNAME


class TestJobsEvents(TestMethodsBase):

    def after_insert(self):
        db = self.connection[MONGO_DBNAME]
        return db._jobs.find_one({"event": self.event_created}) is not None

    def test_event_added_for_jobs(self):
        devent = DummyEvent(self.after_insert, True)
        self.apiapp.on_inserted__jobs += devent

        self.post_dummy_book_created_subscription()

        self.post_dummy_book(self.book_name)

        self.assertEqual(self.event_created, devent.called[0][0]['event'])