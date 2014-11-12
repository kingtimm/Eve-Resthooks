#Eve-Resthooks

## Introduction

Eve-Resthooks = Eve + Rest Hooks

[Rest hooks](http://resthooks.org/) allow your Eve app to notify other services/clients of operations on your Eve API
app via REST. Follow the link to find out more information. In the rest hooks authors' own words:

>REST Hooks itself is not a specification, it is a collection of patterns that treat webhooks like subscriptions. 
These subscriptions are manipulated via a REST API just like any other resource.



## Jobs

#Running

##Running the Example

To run the example, you will need to have a mongodb setup and change the settings.py to reflect your mongo server's
settings.

It may require creating a user for the db as well:

``` 
db.addUser( { user: "user", pwd: "user", roles: [ "readWrite" ] } )
```

##Running the Tests
The tests currently setup a db according to the settings in testsettings.py. You will need to have a mongo server
running to run the tests.
