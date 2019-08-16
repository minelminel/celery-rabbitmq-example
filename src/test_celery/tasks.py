import time
import requests

from .celery import celery_app
from .utils import NPRParser

POLITE_WAIT = 0
URL_FOR_STATUS = 'http://127.0.0.1:8080/status'
URL_FOR_QUEUE = 'http://127.0.0.1:8080/queue'
URL_FOR_CONTENT = 'http://127.0.0.1:8080/content'


@celery_app.task(name='tasks.holding_tank')
def holding_tank(url):
    # print(f'[HOLDING_TANK] {url}')
    return sorting_hat(url)


@celery_app.task(name='tasks.sorting_hat')
def sorting_hat(url):
    try:
        r = requests.get(URL_FOR_STATUS)
    except:
        # print(f'[SORTING_HAT] * Unable to connect to API/status ({url})')
        return f'[SORTING_HAT] * Unable to connect to {URL_FOR_STATUS} ({url})'
    enabled = r.json().get('enabled')
    # print(f'[SORTING_HAT] enabled={enabled} ... {url}')
    if enabled is True:
        time.sleep(POLITE_WAIT)
        return fetch_url(url)
    elif enabled is False:
        report = dict(url=url, status='READY')
        return archive_url(report)


@celery_app.task(name='tasks.fetch_url')
def fetch_url(url):
    r = requests.get(url)
    if r.status_code is 200:
        # print(f'[FETCH_URL] status={r.status_code} ... {url} ')
        return extract_content(r)
    else:
        # print(f'[FETCH_URL] * status={r.status_code} ... {url}')
        return f'[FETCH_URL] * status={r.status_code} ... {url}'


@celery_app.task(name='tasks.extract_content')
def extract_content(response):
    print('[EXTRACT_CONTENT]')
    npr = NPRParser(response)
    content = npr.extract_content()
    return archive_content(content)


@celery_app.task(name='tasks.archive_content')
def archive_content(content):
    urls = content.pop('url')
    r = requests.post(URL_FOR_CONTENT, json=content)
    # print(f'[ARCHIVE_CONTENT] status={r.status_code}')
    report = dict(url=content['origin'],status='DONE')
    # fb = feed_back(dict(url=urls))
    return archive_url(report)


@celery_app.task(name='tasks.archive_url')
def archive_url(report):
    try:
        r = requests.put(URL_FOR_QUEUE, json=report)
        # print(f'[ARCHIVE_URL] status_code={r.status_code}')
        return r.status_code
    except:
        # print(f'[ARCHIVE_URL] * Unable to connect to API')
        return f'[ARCHIVE_URL] * Unable to connect to {URL_FOR_QUEUE}'


# @celery_app.task(name='tasks.feed_back')
# def feed_back(urls):
#     DEBUG_MODE = False
#     if not DEBUG_MODE:
#         r = requests.post(URL_FOR_QUEUE, json=urls)
#         # print(f'[FEED_BACK] status={r.status_code}')
#     else:
#         print(' * * [DEBUG MODE ENABLED] * *')
#         pass
