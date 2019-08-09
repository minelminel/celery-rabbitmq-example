# TODO

- do: add method to allow dumping of URL Archive to task queue
- do: get status endpoint url from a more maintainable location such as a config or and environment variable (celery.tasks.sorting_hat)
- make: Content database class
- make: Content marshmallow schema






# figured it out -- workflow

URLs that need to be visited are added to 'all_urls' queue. This queue is set to run until it is empty, and will send tasks to workers greedily. Within this task, we will call one of two child functions.

- if Enabled=True, we dispatch the url to a task which visits the site and scrapes the page. This task in turn dispatches the scraped data to a task which parses the content for any information we may be extracting. The result of this task is stored in our custom 'result_content' database table.  

- if Enabled=False, instead of sending the url to the task which visits the site, we instead add a new item to our 'url_queue' database table. Since this action will be much faster than actually visiting and extracting the content, we should in theory be able to empty the queue in this way relatively quickly. Once the queue has no more tasks, naturally, our process 'pauses'.

As far as how we decide which path to take--scraping or saving--we have several options. We could first have the task send a request to our own special API endpoint which will return either True or False, but this doubled the amount of requests we have to send in total and can cause an undue burden on our service. A better option would be some way to access the ActionState object from within the task, which would have an attribute specifying whether or not the service is active.

When we want to start the service, we call a method on our 'url_queue' database which queries ALL rows where the 'queued' column is False and adds the urls to the queue one by one. This process itself could be an async task. For each url added to the queue, it is designated as having been processed by changing the 'queued' column to True. This serves as a failsafe backup in the event that all urls are lost in the process of transferring them to the queue.

URLs can be directly added to the 'url_queue' database by means of an API endpoint. These urls are immediately added to the queue ONLY if the service is currently enabled. In the case that they are 'shotgunned' to the queue, the 'queued' column is set to True, otherwise this reverts to the default of False.

There will be an API endpoint for querying the 'result_content' database which will store our extracted data such as headline, text, captions, etc. This should work as a GraphQL protocol, where the user specifies which content fields they need, as well as the number of rows to query.

In addition, one API endpoint should return information about the number of rows in our 'url_queue' database and how many have been queued or are still waiting, as well as the number of tasks in each of the queues, and finally what the current state of the service is--enabled or disabled.

We will have to come up with some sort of method for keeping track of which results have been requested by external services. Perhaps using the same endpoint as our GraphQL api but with a POST request will modify a column called 'last_retrieved', which would have a default of None. We can request rows which have never been requested before, or request rows which were last requested BEFORE a specified date, although this could be an expensive operation.
