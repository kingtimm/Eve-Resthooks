import json
import bson
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


def is_filter_match(resource, subscription, item):

    filter_string = subscription.get('filter', "{}")
    filter = json.loads(filter_string)

    # potentially find a match where filtering is done by id.
    if filter.get("_id") and item.get('_id'):
        if bson.ObjectId(item['_id']) == bson.ObjectId(filter['_id']):
            return item

    # potentially find a match where item's updated value matched the filter.
    if not item.get('_id'):
        for k, v in filter.items():
            if item.get(k):
                if v == item.get(k):
                    continue
                else:
                    break
            else:
                break
        else:
            return item

    # potentially find a match where item's original value matched the filter, but may have gotten a new one..
    if item.get('_id') and not filter.get("_id"):
        filter.update({"_id": bson.ObjectId(item['_id'])})
        # resources = apiapp.data.driver.db[resource]
        # return resources.find_one(filter)
        for k, v in filter.items():
            if item.get(k):
                if v == item.get(k):
                    continue
                else:
                    break
            else:
                break
        else:
            return item


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


def on_updated(resource_name, updates, original):
    if not resource_name.startswith("__"):  # protection from dunder resources...maybe
        if resource_name != "subscriptions":  # circular protection? maybe implement this later
            subscriptions = apiapp.data.driver.db['subscriptions']
            event_string = "{0}.updated".format(resource_name)
            relevant_subscriptions = subscriptions.find({"event": event_string})

            for sub in relevant_subscriptions:
                if is_filter_match(resource_name, sub, updates) or is_filter_match(resource_name, sub, original):
                    payload = {
                        "claimed": False,
                        "status": 0,
                        "target_url": sub['target_url'],
                        "result": "",
                        "payload": dict(updates=updates, original=original),
                        "event": event_string
                    }

                    result = eve_post_internal("_jobs", payload)


def on_replaced(resource_name, new_item, original):
    if not resource_name.startswith("__"):  # protection from dunder resources...maybe
        if resource_name != "subscriptions":  # circular protection? maybe implement this later
            subscriptions = apiapp.data.driver.db['subscriptions']
            event_string = "{0}.replaced".format(resource_name)
            relevant_subscriptions = subscriptions.find({"event": event_string})

            for sub in relevant_subscriptions:
                if is_filter_match(resource_name, sub, new_item) or is_filter_match(resource_name, sub, original):
                    payload = {
                        "claimed": False,
                        "status": 0,
                        "target_url": sub['target_url'],
                        "result": "",
                        "payload": dict(new=new_item, original=original),
                        "event": event_string
                    }

                    result = eve_post_internal("_jobs", payload)
