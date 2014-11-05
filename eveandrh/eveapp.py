from eve.io.mongo import Validator
from eveandrh.controllers import subscriptions
from flask import current_app as app


class Eveandrh():
    def __init__(self, Eveapp):
        self.eveapp = Eveapp
        self.patch_existing_validator()
        self.add_rest_hook_events()

    def add_rest_hook_events(self):
        self.eveapp.on_inserted += subscriptions.on_created

    def patch_existing_validator(self):
        """Patches whatever validator class is in use with the following additions
        """
        cls = self.eveapp.validator

        class EveandrhValidator(cls):
            def _validate_nodupesubs(self, nodupesubs, field, value):
                if nodupesubs and self.resource == "subscriptions":
                    query = {"event": self.document['event'], "target_url": self.document['target_url']}
                    if app.data.find_one(self.resource, None, **query):
                        self._error(field,
                                    "There is already a subscription for {0} to hit {1}".format(self.document['event'],
                                                                                                self.document[
                                                                                                    'target_url']))

        self.eveapp.validator = EveandrhValidator