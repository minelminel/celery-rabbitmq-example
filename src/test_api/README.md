# API Overview

All urls that are processed by the service must go through the database. By default, the urls are assigned the default value for status: `READY`. When urls are dispatched to the celery task queue, their status is changed to `TASKED`. The original url from which the content is scraped is referred to as the `origin`. When this `origin` url is returned to the API Queue Archive by means of saving the state as a result of the `enabled` value being `False`, their status is reset to `READY`, so that they can be re-dispatched again in the future. When the `origin` url returns after the process of scraping a site has been completed, their status is set to `DONE` so they can remain as a means of discarding repeated urls.

# Adding URLs `/queue POST I`
When urls are processed, they are each checked against the database to see whether they are new or if they have been seen before. In the case where the url is present in the database, no matter its `status`, it is discarded. Once we have reduced the list down to only contain entries we have not seen before, we add each of them to the database with the default status of `READY`. At the end of this operation, we have a list of all urls that we should add to the queue.
```python
# normally formatted as a list, many=True
data, errors = urls_schema.dump(request.get_json())
if errors:
  return reply_errors(errors)
elif data:
  reply = []
  for url in data:
    result = db.session.queue(Queue).filter_by(url=url['url']).first()
    if not result:
      _data, _ = url_schema.dump(data)
      q = Queue(_data) # should have default status of 'READY'
      db.session.add(q)
      db.session.commit()
      reply.append(q)
  # yields reply[] of urls which we are good to add to queue
  return reply
```

# Dispatching URLs `/queue POST II`
After urls are initially processed to remove duplicates, we are left with a list of the remaining valid urls which we wish to dispatch to the celery task queue. For each item in the list, we query the database by url and receive a result object. We must set the `status` value to `TASKED` and save the entry, only after this can we release the url by calling task.delay(url)
```python
# reply[] from above
for url in reply:
  result = db.session.query(Queue).filter_by(url=url['url']).first()
  result.status = 'TASKED'
  db.session.commit()
  tasks.holding_tank.delay(url['url'])
return reply_success(reply)
```

# Receiving URLs from the task queue `/queue PUT`
When urls are in the task queue, the task first sends a request to the `/status` endpoint to determine which course of action we should take. If `enabled=False`, we want to immediately return the url to the Api so that we can save it for later. We assign the `status` key to `READY` and send our request. Once this request is received, we update the database to reflect this change. These urls can later be dispatched again to the task queue, and should the service be `enabled`, can be fetched and scraped.  
If `enabled=True` at the time of our request, we pass the url along to the next task component and continue the process of scraping and extracting content. At the end of this chain of processes we will again send a request to the Api such that we may record our visiting the url's location. We prepare a request which has the `status` value set to `DONE` and this record is updated in the database.
```python
''' celery.tasks '''
r = requests.get(url_for_status_get)
if r.status_code is not 200:
  raise IOError(f'Unable to get status from api endpoint (status={r.status_code})')
else:
  is_enabled = r.json().get('enabled', False)
if is_enabled:
  # pass go
  return fetch_url(url)
else:
  # go directly to jail, do not collect $200
  return archive_url(url, status='READY')


''' app.views '''
# only ever a single url at a time, many=False
data, errors = url_schema.load(request.get_json())
if errors:
  return reply_error(errors)
elif data:
  result = db.session.queue(Queue).filter_by(url=data['origin'])
  result.status = 'DONE'
  db.session.commit()
  _data, _ = queue_schema.dump(db.session.query(Queue).filter_by(id=result).first())
  if _errors:
    return reply_error(_errors)
  elif _data:
    return reply_success(_data)

```

# Dumping the database to the task queue `/status POST (when enabled is set to True)`
In the case that we have disabled our service, all of the contents of the task queue will be saved into the database. Naturally, once we enable the service we will need a method by which to add all these urls back to the task queue. To do this, we must query the database for all rows where the `status` value is `READY`. We are returned a list of result objects from which we may in turn release to the task queue. At this point, we defer to the logic laid out in the `"Dispatching URLs"` section above.
```python
# called as a function after the status is enabled

# get list of all urls from db where status='READY'
reply = []
result = db.session.query(Queue).filter_by('READY').all()
for r in result:
  r.status = 'TASKED'
  db.session.commit()
  _data, _ = url_schema.dump()
  holding_tank(_data['url'])
  reply.append(_data)
return reply_success(reply)

```



# Api Guide

### `GET` /queue
| Arg | Type     | Default     |
| :------------- | :------------- | :------------- |
| limit       | Integer     |  10   |
| status       | List       |   [READY, TASKED, DONE]  |
