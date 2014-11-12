# Subscriptions

The subscriptions endpoint is designed according to the resthooks.org docs to allow you to manipulate subscriptions via
REST.

These operations may not be in order. Be sure to double check your etags.

## Params

### event
The event specifies what db operations to subscribe to. It is in the format of:

RESOURCE.OPERATION

Where:

RESOURCE = the resource you want to subscribe to Example: books

OPERATION = the operation you want to subscribe to: created, replaced, updated, or deleted.

### target_url
The remote url that you want to hit with a notification payload.

### filter
A JSON dictionary of keys and values you want to filter on:

Examples:

    "{'_id':'548729387498729879873487987'}"
    
    "{'name':'A certain book title'}"

Only items with that resource will be returned.

## Resource Operations

### Create (POST)

#### Request

    curl -X POST 
        -H 'Content-Type: application/json' 
        -d '{"event":"books.created","target_url":"http://remoteserver.bogus/notifications"}' 
        http://localhost:5000/api/v1/subscriptions

#### Result
    {
        "_updated": "...",
        "_id": "546242075eb55f2190f711d0",
        "_etag": "e4f693d426a481ee3feb71f275d564741790c330",
        "_links": {
          "self": {
                "href": "/subscriptions/546242075eb55f2190f711d0",
                "title": "Subscription"
            }
        },
        "_status": "OK",
        "_created": "..."
    }

### Replace (PUT)

#### Request

    curl -X PUT 
        -H 'Content-Type: application/json'
        -H 'If-Match: b1f55bdad87b386b0477b9bb5953aec6364dc12a'
        -d '{"event":"books.created", "target_url":"http://remoteserver.bogus/notifications"}' 
        http://localhost:5000/api/v1/subscriptions/546242075eb55f2190f711d0

#### Result

    {
        "_updated": "...", 
        "_links": {
            "self": {
                "title": "Subscription", 
                "href": "/subscriptions/546242075eb55f2190f711d0"
            }
        }, 
        "_etag": "1fb8023c33fbff2836de2309c1bdc709d757997c", 
        "_status": "OK", 
        "_created": "...", 
        "_id": "546242075eb55f2190f711d0"
    }
    
### Update (PATCH)

#### Request

    curl -X PATCH 
        -H 'Content-Type: application/json'
        -H 'If-Match: e4f693d426a481ee3feb71f275d564741790c330'
        -d '{"target_url":"http://backupremoteserver.bogus/notifications"}' 
        http://localhost:5000/api/v1/subscriptions/546242075eb55f2190f711d0

#### Result

    {
        "_id": "546242075eb55f2190f711d0", 
        "_updated": "...", 
        "_etag": "b1f55bdad87b386b0477b9bb5953aec6364dc12a", 
        "_links": {
            "self": {
                "href": "/subscriptions/546242075eb55f2190f711d0", 
                "title": "Subscription"
            }
        }, 
        "_status": "OK", 
        "_created": "..."
    }
    
### Delete (DELETE)

#### Request

    curl -X DELETE 
        -H 'Content-Type: application/json'
        -H 'If-Match: 1fb8023c33fbff2836de2309c1bdc709d757997c'
        http://localhost:5000/api/v1/subscriptions/546242075eb55f2190f711d0

#### Result

    {}

### List (GET)

#### Request

    curl -X GET 
        -H 'Content-Type: application/json' 
        http://localhost:5000/api/v1/subscriptions

#### Response

    {
        "_links": {
            "parent": {
                "title": "home",
                "href": "/"
            },
            "self": {
                "title": "subscriptions",
                "href": "/subscriptions"
            }
        },
        "_meta": {
            "page": 1,
            "max_results": 25,
            "total": 2
        },
        "_items": [{
            "target_url": "http://remoteurl/notifications",
            "_links": {
                "self": {
                    "title": "Subscription",
                    "href": "/subscriptions/546241b25eb55f2190f711cf"
                }
            },
            "_etag": "72c5592b02f112264637475d1ee54697bf76a2c7",
            "event": "books.created",
            "_updated": "...",
            "_created": "...T",
            "_id": "546241b25eb55f2190f711cf"
        },
        {
            "target_url": "http://remoteserver.bogus/notifications",
            "_links": {
                "self": {
                    "title": "Subscription",
                    "href": "/subscriptions/5462445d5eb55f2190f711d1"
                }
            },
            "_etag": "ff2838c5863ba623f870f6d4237f431d2945c2b6",
            "event": "books.created",
            "_updated": "...",
            "_created": "...",
            "_id": "5462445d5eb55f2190f711d1"
        }]
    }