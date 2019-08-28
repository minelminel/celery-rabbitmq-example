import time
import requests

import artifice.scraper.config.settings as settings
from .celery import celery_app
from .parsers import NPRParser
from .util import report_done, report_ready


def throw(error, *args, **kwargs):
    raise error(*args, **kwargs)


@celery_app.task(name='tasks.holding_tank')
def holding_tank(url, **kwargs):
    return sorting_hat(url, **kwargs)


@celery_app.task(name='tasks.sorting_hat')
def sorting_hat(url, **kwargs):
    try:
        r = requests.get(settings.URL_FOR_STATUS)
    except:
        throw(ConnectionError, 'Unable to determine whether service is enabled', settings.URL_FOR_STATUS)
    enabled = r.json().get('enabled')
    polite = r.json().get('polite')
    if enabled is True:
        time.sleep(polite)
        return fetch_url(url, **kwargs)
    elif enabled is False:
        return archive_url(report_ready(url), **kwargs)


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
    r = requests.post(settings.URL_FOR_CONTENT, json=content)
    fb = feed_back(content)
    url = content.get('origin')
    return archive_url(report_done(url), content=r.status_code, feedback=fb, **kwargs)


@celery_app.task(name='tasks.archive_url')
def archive_url(json_data, **kwargs):
    r = requests.put(settings.URL_FOR_QUEUE, json=json_data)
    return r.status_code, {**kwargs}


@celery_app.task(name='tasks.feed_back')
def feed_back(content):
    json_data = dict(url=content.get('url'))
    r = requests.post(settings.URL_FOR_QUEUE, json=json_data)
    return r.status_code
