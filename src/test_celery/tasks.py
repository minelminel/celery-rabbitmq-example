import time
import requests

from .celery import app
from .utils import pour_soup, NPRParser

URL_FOR_STATUS = 'http://127.0.0.1:8080/status'
URL_FOR_ARCHIVE = 'http://127.0.0.1:8080/queue'
URL_FOR_CONTENT = 'http://127.0.0.1:8080/content'


@app.task(name='tasks.holding_tank')
def holding_tank(url):
    print(f'[HOLDING_TANK] {url}')
    return sorting_hat(url)


@app.task(name='tasks.sorting_hat')
def sorting_hat(url):
    try:
        r = requests.get(URL_FOR_STATUS)
    except ConnectionError as e:
        print(f'[SORTING_HAT] * Unable to connect to API/status ({url})')
        return
    enabled = r.json().get('enabled')
    print(f'[SORTING_HAT] enabled={enabled} ... {url}')
    if enabled is True:
        return fetch_url(url)
    elif enabled is False:
        return archive_url(url)


@app.task(name='tasks.fetch_url')
def fetch_url(url):
    r = requests.get(url)
    if r.status_code is 200:
        print(f'[FETCH_URL] status={r.status_code} ... {url} ')
        return extract_content(url, r)
    else:
        print(f'[FETCH_URL] * status={r.status_code} ... {url}')
        return False


@app.task(name='tasks.extract_content')
def extract_content(url, response):
    print('[EXTRACT_CONTENT]')
    soup = pour_soup(response)
    npr = NPRParser(url, response)
    content = npr.extract_content()
    return archive_content(**content)


@app.task(name='tasks.archive_content')
def archive_content(**kwargs):
    r = requests.post(URL_FOR_CONTENT, json=dict(**kwargs))
    success = True if r.status_code is 200 else False
    print(f'[ARCHIVE_CONTENT] success={success}')
    return success


@app.task(name='tasks.archive_url')
def archive_url(url):
    print(f'[ARCHIVE_URL] {url}')
    try:
        r = requests.put(URL_FOR_ARCHIVE, json=dict(url=url))
    except ConnectionError as e:
        print(f'[ARCHIVE_URL] * Unable to connect to API/url ({url})')
        success = False
    success = True if r.status_code is 200 else False
    print(f'[ARCHIVE_URL] success={success} ... {url}')
    return success
