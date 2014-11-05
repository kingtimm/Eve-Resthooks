from flask import current_app as apiapp, jsonify, abort
from eve.methods.post import post_internal as eve_post_internal


def get_eve_event_name(event_string):

    endpoint, verb = event_string.split(".")

    verb_map = {
        "created": "inserted",
        "replaced": "replaced",
        "updated": "updated",
        "deleted": "deleted",
    }

    return endpoint, verb_map[verb]


def on_subscriptions_insert(items):
    for item in items:
        event, target = item['event'], item['target_url']
        subscriptions = apiapp.data.driver.db['subscriptions']
        matching_subscription = subscriptions.find({"event": event, "target_url": target})
        if matching_subscription:
            abort(409, "Subscription with that event and target already exists")


def on_created(resource_name, items):  # todo add protection from hidden resources and stuff
    if not resource_name.startswith("__"):  # protection from dunder resources...maybe
        if resource_name != "subscriptions":  # circular protection? maybe implement this later
            subscriptions = apiapp.data.driver.db['subscriptions']
            for item in items:

                event_string = "{0}.created".format(resource_name)
                relevant_subscriptions = subscriptions.find({"event": event_string})

                for sub in relevant_subscriptions:

                    payload = {
                        "claimed": False,
                        "status": 0,
                        "target_url": sub['target_url'],
                        "result": "",
                        "payload": item,
                        "event": event_string
                    }

                    result = eve_post_internal("_jobs", payload)
