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

# Your Own Events

Instead of polling the _jobs endpoint, you could write your own event handlers when there is a job added. I.E.

- Add it to a celery queue
- Add to redis
- Run your own little threadpool, asyncio, async requests, etc.

This can be done by using the Events built into Eve. (I actually started writing my own version, but this is better).

    def add_task(items):
        for item in items:
            Task(item)
            
    eveapp.on_inserted__jobs += add_task
    
Adding this event handler will send the job right into your own function.

It'll have a field for ```_id``` and ```_links``` so your function could even report back to the db that the task was
completed using the payload above.
