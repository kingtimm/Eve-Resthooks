# Jobs

## Current State
Jobs refers to notification jobs based on subscriptions to certain database operations.

Currently, the jobs are added to an endpoint. This allows you to build decoupled applications with your own workers.

Resthook workers can be simple or complex, based on these reasons:

- [Performance] (http://resthooks.org/docs/performance/)
- [Security] (http://resthooks.org/docs/security/)
- [Retries] (http://resthooks.org/docs/retries/)

For even more reasons, check out this blog post: [HTTP Requests are Hard] (http://www.mobify.com/blog/http-requests-are-hard/)

## Notification Data

The following data is passed with each:

"claimed": False,
                "status": 0,
                "target_url": sub['target_url'],
                "result": "",
                "payload": item,
                "event": event_string

### claimed

Boolean to determine whether a worker has claimed the job or not.

### status

HTTP Status Code returned when the notification was performed by the worker.

### target_url

The url to hit with the notification data

### result

The raw response when the notification was performed by the worker

### event

The event name that was used to show it

### payload

This has its own section as its important.

## Payload

The payload data sent in each notification is the data resulting from the DB op.

There are two types of operational payloads:

### changed Payload

A changed payload is sent when the database operation is either Replaced or Updated.

### existence Payload

An existence payload is sent when the database operation is either Created or Deleted.


