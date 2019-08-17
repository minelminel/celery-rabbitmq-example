import time
import requests

from .celery import celery_app
from .utils import NPRParser

POLITE_WAIT = 3
URL_FOR_STATUS = 'http://127.0.0.1:8080/status'
URL_FOR_QUEUE = 'http://127.0.0.1:8080/queue'
URL_FOR_CONTENT = 'http://127.0.0.1:8080/content'

def raise_error(error, *args, **kwargs):
    raise error(*args, **kwargs)


@celery_app.task(name='tasks.holding_tank')
def holding_tank(url):
    # print(f'[HOLDING_TANK] {url}')
    return sorting_hat(url)


@celery_app.task(name='tasks.sorting_hat')
def sorting_hat(url):
    r = requests.get(URL_FOR_STATUS)
    enabled = r.json().get('enabled')
    # print(f'[SORTING_HAT] enabled={enabled} ... {url}')
    if enabled is True:
        time.sleep(POLITE_WAIT)
        return fetch_url(url)
    elif enabled is False:
        return archive_url(url, 'READY')


@celery_app.task(name='tasks.fetch_url')
def fetch_url(url):
    r = requests.get(url)
    # print(f'[FETCH_URL] status={r.status_code} ... {url} ')
    return extract_content(r)


@celery_app.task(name='tasks.extract_content')
def extract_content(response):
    # print('[EXTRACT_CONTENT]')
    npr = NPRParser(response)
    content = npr.extract_content()
    # convert the content to strings
    return archive_content(content)


@celery_app.task(name='tasks.archive_content')
def archive_content(content):
    # urls = content.pop('url')
    r = requests.post(URL_FOR_CONTENT, json=content)
    print(f'[ARCHIVE_CONTENT]\tstatus_code={r.status_code}\t{content}')
    return archive_url(content.get('origin'),'DONE')


@celery_app.task(name='tasks.archive_url')
def archive_url(url, status):
    json_data = dict(url=url,status=status)
    r = requests.put(URL_FOR_QUEUE, json=json_data)
    print(f'[ARCHIVE_URL]\tstatus_code={r.status_code}\t{json_data}')
    return r.status_code
