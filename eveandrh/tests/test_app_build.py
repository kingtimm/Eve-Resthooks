from eveandrh.tests.base import TestBaseMinimal


class TestAppBuild(TestBaseMinimal):
    def test_building_of_app(self):

        result = self.local_client.get('/')

        self.assertTrue(self.apiapp)

    def test_rest_hook_created_added(self):

        self.assertTrue(hasattr(self.apiapp, "on_inserted"))

    def test_validator_has_method(self):

        name = repr(self.apiapp.validator)

        self.assertTrue("EveandrhValidator" in name)