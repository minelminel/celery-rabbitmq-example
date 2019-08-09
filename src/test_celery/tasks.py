# from __future__ import absolute_import
import time
import requests

from test_celery.celery import app


'''
    # # TO HOLD OFF ON RETURNING UNTIL CHILD TASKS RETURN:
    reply = another_task(arg)
    return reply
    # # TO RETURN RESULT BEFORE PASSING TO CHILD TASK:
    return another_task(arg)
'''

@app.task(name='tasks.holding_tank')
def holding_tank(url):
    print(f'holding tank started for {url}')
    print(f'holding tank finished for {url}')
    return sorting_hat(url)


@app.task(name='tasks.sorting_hat')
def sorting_hat(url):
    print(f'sorting_hat task started for {url}')
    r = requests.get('http://127.0.0.1:8080/status')
    enabled = r.json().get('enabled')
    print(f'sorting_hat Enabled={enabled} for {url}')
    if enabled:
        print(f'sending {url} to tasks.fetch_url')
        return fetch_url(url)
    else:
        print(f'sending {url} to tasks.archive_url')
        return archive_url(url)


@app.task(name='tasks.fetch_url')
def fetch_url(url):
    print(f'fetch_url started for {url}')
    r = requests.get(url)
    if r.status_code == 200:
        print(f'fetch_url for {url} status_code={r.status_code}')
        return extract_content(r)
    else:
        print(f'fetch_url failed with {r.status_code} for {url}')
        return False



@app.task(name='tasks.extract_content')
def extract_content(response):
    print('extract_content started')
    content = response.content
    # return **content
    print('extract_content finished')
    return archive_content(content)


@app.task(name='tasks.archive_content')
def archive_content(*args):
    print('archive_content started')
    # save to database
    success = True
    print(f'archive_content finished, success={success}')
    return success


@app.task(name='tasks.archive_url')
def archive_url(url):
    print(f'archive_url started for {url}')
    # save to database
    success = True
    print(f'archive_url finished for {url}, success={success}')
    return success
