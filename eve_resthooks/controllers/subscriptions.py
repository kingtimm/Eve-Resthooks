import json
import bson
from flask import current_app as apiapp
from eve.methods.post import post_internal as eve_post_internal


def get_eve_event_name(event_string):
    """Translates CRUD to Database ops names.
    """
    endpoint, verb = event_string.split(".")

    verb_map = {
        "created": "inserted",
        "replaced": "replaced",
        "updated": "updated",
        "deleted": "deleted",
    }

    return endpoint, verb_map[verb]


def is_subscribable_endpoint(resource_name):
    """ Protection from dunder resources (future)

    Protection from subscribing to the subscriptions endpoint (seems like a bad idea).
    """
    return (not resource_name.startswith("__")) and (resource_name != "subscriptions")


def _compare_dictionaries(filter, item):
    """Compares the filter dictionary criteria with the keys and values in the actual item.

    This is slower than the commented one below. However, the one below doesn't like sub-dictionaries
    """
    for k, v in filter.items():
        if item.get(k):
            if v == item.get(k):
                continue
            else:
                return False
        else:
            return False
    else:
        return item

# def _compare_dictionaries(filter, item):
#     """The intersection of the dictionaries is where the keys and values are the same.
#
#     This ensures that the number of items in the intersection is the same as the number of filter criteria.
#
#     """
#     if len(set(filter.items()) & set(item.items())) == len(filter.items()):
#         return item


def is_filter_match(resource, subscription, item):
    """Checks if the db operation's item meets the criteria of a certain subscription.

    """
    filter_string = subscription.get('filter', "{}")
    filter = json.loads(filter_string)

    # potentially find a match where filtering is done by id.
    if filter.get("_id") and item.get('_id'):
        if bson.ObjectId(item['_id']) == bson.ObjectId(filter['_id']):
            return item

    # potentially find a match where item's updated value matched the filter.
    if not item.get('_id'):
        return _compare_dictionaries(filter, item)

    # potentially find a match where item's original value matched the filter, but may have gotten a new one..
    if item.get('_id') and not filter.get("_id"):
        filter.update({"_id": bson.ObjectId(item['_id'])})
        # resources = apiapp.data.driver.db[resource]
        # return resources.find_one(filter)
        return _compare_dictionaries(filter, item)


def _post_job_with_payload(payload):
    post_result, _, _, _ = eve_post_internal("_jobs", payload)

    return post_result


def _post_jobs_for_created_or_deleted_item(event_string, item, resource_name, subscriptions):
    relevant_subscriptions = subscriptions.find({"event": event_string})
    for sub in relevant_subscriptions:
        if is_filter_match(resource_name, sub, item):
            payload = {
                "claimed": False,
                "status": 0,
                "target_url": sub['target_url'],
                "result": "",
                "payload": item,
                "event": event_string
            }

            _post_job_with_payload(payload)


def _post_jobs_for_existing_item_that_changed(event_string, new, original, resource_name, subscriptions):
    relevant_subscriptions = subscriptions.find({"event": event_string})
    for sub in relevant_subscriptions:
        if is_filter_match(resource_name, sub, new) or is_filter_match(resource_name, sub, original):
            payload = {
                "claimed": False,
                "status": 0,
                "target_url": sub['target_url'],
                "result": "",
                "payload": dict(new=new, original=original),
                "event": event_string
            }

            _post_job_with_payload(payload)


def on_created(resource_name, items):
    if is_subscribable_endpoint(resource_name):
        subscriptions = apiapp.data.driver.db['subscriptions']
        for item in items:
            event_string = "{0}.created".format(resource_name)
            _post_jobs_for_created_or_deleted_item(event_string, item, resource_name, subscriptions)


def on_updated(resource_name, new, original):
    if is_subscribable_endpoint(resource_name):
        subscriptions = apiapp.data.driver.db['subscriptions']
        event_string = "{0}.updated".format(resource_name)
        _post_jobs_for_existing_item_that_changed(event_string, new, original, resource_name, subscriptions)


def on_replaced(resource_name, new, original):
    if is_subscribable_endpoint(resource_name):
        subscriptions = apiapp.data.driver.db['subscriptions']
        event_string = "{0}.replaced".format(resource_name)
        _post_jobs_for_existing_item_that_changed(event_string, new, original, resource_name, subscriptions)


def on_deleted_item(resource_name, item):
    if is_subscribable_endpoint(resource_name):
        subscriptions = apiapp.data.driver.db['subscriptions']
        event_string = "{0}.deleted".format(resource_name)
        _post_jobs_for_created_or_deleted_item(event_string, item, resource_name, subscriptions)

