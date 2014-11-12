from eve_resthooks.domain import DOMAIN
from eve_resthooks.controllers import subscriptions
from flask import current_app as app
from eve_resthooks.exceptions import DomainConflictException


class EveRestHooks():
    def __init__(self, Eveapp):
        """Patches an eve app to use Rest Hooks

        :param Eveapp: An Eve App to modify to use Rest Hooks
        """
        self.eveapp = Eveapp
        self.patch_existing_domain()
        self.patch_existing_validator()
        self.add_rest_hook_events()

    def add_rest_hook_events(self):
        """Adds eve Events handlers for crud operations on the db.
        """
        self.eveapp.on_inserted += subscriptions.on_created
        self.eveapp.on_updated += subscriptions.on_updated
        self.eveapp.on_replaced += subscriptions.on_replaced
        self.eveapp.on_deleted_item += subscriptions.on_deleted_item

    def patch_existing_validator(self):
        """Patches whatever validator class is in use with the following additions
        """
        cls = self.eveapp.validator

        class EveResthooksValidator(cls):
            def _validate_nodupesubs(self, nodupesubs, field, value):
                if nodupesubs and self.resource == "subscriptions":
                    query = {"event": self.document['event'], "target_url": self.document['target_url']}
                    if app.data.find_one(self.resource, None, **query):
                        self._error(field,
                                    "There is already a subscription for {0} to hit {1}".format(self.document['event'],
                                                                                                self.document[
                                                                                                    'target_url']))

        self.eveapp.validator = EveResthooksValidator

    def patch_existing_domain(self):
        """Patches the domain currently in use to add the jobs and subscriptions endpoints
        """

        overlap = set(self.eveapp.config["DOMAIN"].keys()).intersection(set(DOMAIN.keys()))

        if not overlap:
            with self.eveapp.app_context():
                self.eveapp.config["DOMAIN"].update(DOMAIN)

            for k in DOMAIN.keys():
                self.eveapp.register_resource(k, DOMAIN[k])
        else:
            raise DomainConflictException()