import time
import requests

# from .celery import celery_app
from .celery import celery_app
from .config import Endpoints
from .parsers import NPRParser

# URL_FOR_STATUS = 'http://127.0.0.1:8080/status'
# URL_FOR_QUEUE = 'http://127.0.0.1:8080/queue'
# URL_FOR_CONTENT = 'http://127.0.0.1:8080/content'
endpoints = Endpoints()


def throw(error, *args, **kwargs):
    raise error(*args, **kwargs)


@celery_app.task(name='tasks.holding_tank')
def holding_tank(url, **kwargs):
    return sorting_hat(url, **kwargs)


@celery_app.task(name='tasks.sorting_hat')
def sorting_hat(url, **kwargs):
    r = requests.get(endpoints.STATUS)
    enabled = r.json().get('enabled')
    politeness = r.json().get('politeness')
    if enabled is True:
        time.sleep(politeness)
        return fetch_url(url, **kwargs)
    elif enabled is False:
        return archive_url(url, 'READY', **kwargs)


@celery_app.task(name='tasks.fetch_url')
def fetch_url(url, **kwargs):
    r = requests.get(url)
    return extract_content(r, **kwargs)


@celery_app.task(name='tasks.extract_content')
def extract_content(response, **kwargs):
    npr = NPRParser(response)
    content = npr.extract_content()
    return archive_content(content, **kwargs)


@celery_app.task(name='tasks.archive_content')
def archive_content(content, **kwargs):
    r = requests.post(endpoints.CONTENT, json=content)
    fb = feed_back(content)
    return archive_url(content.get('origin'), 'DONE', feedback=fb, **kwargs)


@celery_app.task(name='tasks.archive_url')
def archive_url(url, status, **kwargs):
    json_data = dict(url=url,status=status)
    r = requests.put(endpoints.QUEUE, json=json_data)
    return r.status_code, {**kwargs}


@celery_app.task(name='tasks.feed_back')
def feed_back(content):
    json_data = dict(url=content.get('url'))
    r = requests.post(endpoints.QUEUE, json=json_data)
    return r.status_code
