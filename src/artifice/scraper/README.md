# TODO

- account for items that are getting lost in the process by retaining a status of 'TASKED' even after all the items are dumped from the celery queue

- iron out the method by which request query args are parsed into a list from a single string, once we have a good method to do this it will probably be reused elsewhere

- figure out a way to add scheduled celery tasks, such that we can create backups of the gathered data.

- create a custom marshmallow field for rendering the utc time as an elapsed time, i.e. "7 minutes ago" when displaying both the queue and content database results

- figure out why the content GET request reverts to the default limit of 10

- use cron job/ scheduled process to monitor the api

- download and customize the Flask monitoringdashboard for use with the service. it is a worthy investment of time to get a robust monitoring solution in place. figure out a way to manage alerts for things like error and request rates/ volumes



---

convert the schemas that handle URLs to employ the built-in URL field

Add a mechanism by which we can delete any orphaned tasks. By symptom of design, inevitably we will sometimes be left with tasks that are registered as "TASKED" in our QUEUE database, but which are marked as such unintentionally. These tasks raise errors during the process of reporting back, and can throw off our picture of the system. We need a DELETE method on the Queue endpoint which will either remove these items from the database, or change these urls to be READY instead of TASKED

~~Every time we add some urls to the main celery task queue, we want to keep track of them somehow such that we can ignore duplicates. We must make a small change to the route where we add items to the task queue--the change being that we first add the item(s) to the database, and release the urls as tasks once they have been added. In the event of an IntegrityError that means that the url has already been seen by the service and we should remove it from the list of items to be added to the queue. This allows us to solve the redundant loop problem posed by the repeated addition of the same url.~~


Ideally with a little more understanding of how request, schema, and sqlalchemy objects play together, we can both eliminate massive segments of code and standardize handling of data in such a way that databases are always safe from errors, by ONLY using marshmallow schemas to handle the loading and dumping objects. updates can even be done with class methods (or maybe static methods if we're just setting a key).



- do: get status endpoint url from a more maintainable location such as a config or and environment variable (celery.tasks.sorting_hat)
- ~~do: add method to allow dumping of URL Archive to task queue~~
- ~~make: Content database class~~
- ~~make: Content marshmallow schema~~

# Workflow - add URLs via API
- convert api url additions to go directly to the celery queue if enabled=True, else add to database
# Workflow - load URLs to celery
- urls are added to the database by default with `tombstone = False`, meaning they still need to be scraped
- when service is `enabled`, we want to query the database for all urls where tombstone is False
- for each url in the results, dump to the `many=True` schema version, ONLY want to show the url k-v pair (include?)
- release url to the `holding_tank` task, if this is successful (should always be) set the corresponding `tombstone` column to True
- return the INT number of entries which were released to the task queue
# Workflow - dump URLs from celery
- url is added to the database with the `tombstone` as its default False value


# Overview

URLs that need to be visited are added to 'all_urls' queue. This queue is set to run until it is empty, and will send tasks to workers greedily. Within this task, we will call one of two child functions.

- if Enabled=True, we dispatch the url to a task which visits the site and scrapes the page. This task in turn dispatches the scraped data to a task which parses the content for any information we may be extracting. The result of this task is stored in our custom 'result_content' database table.  

- if Enabled=False, instead of sending the url to the task which visits the site, we instead add a new item to our 'url_queue' database table. Since this action will be much faster than actually visiting and extracting the content, we should in theory be able to empty the queue in this way relatively quickly. Once the queue has no more tasks, naturally, our process 'pauses'.

As far as how we decide which path to take--scraping or saving--we have several options. We could first have the task send a request to our own special API endpoint which will return either True or False, but this doubled the amount of requests we have to send in total and can cause an undue burden on our service. A better option would be some way to access the ActionState object from within the task, which would have an attribute specifying whether or not the service is active.

When we want to start the service, we call a method on our 'url_queue' database which queries ALL rows where the 'queued' column is False and adds the urls to the queue one by one. This process itself could be an async task. For each url added to the queue, it is designated as having been processed by changing the 'queued' column to True. This serves as a failsafe backup in the event that all urls are lost in the process of transferring them to the queue.

URLs can be directly added to the 'url_queue' database by means of an API endpoint. These urls are immediately added to the queue ONLY if the service is currently enabled. In the case that they are 'shotgunned' to the queue, the 'queued' column is set to True, otherwise this reverts to the default of False.

There will be an API endpoint for querying the 'result_content' database which will store our extracted data such as headline, text, captions, etc. This should work as a GraphQL protocol, where the user specifies which content fields they need, as well as the number of rows to query.

In addition, one API endpoint should return information about the number of rows in our 'url_queue' database and how many have been queued or are still waiting, as well as the number of tasks in each of the queues, and finally what the current state of the service is--enabled or disabled.

We will have to come up with some sort of method for keeping track of which results have been requested by external services. Perhaps using the same endpoint as our GraphQL api but with a POST request will modify a column called 'last_retrieved', which would have a default of None. We can request rows which have never been requested before, or request rows which were last requested BEFORE a specified date, although this could be an expensive operation.
