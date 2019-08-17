import unittest
import os
import requests

def make_url(*args):
    url = 'http://localhost:8080'
    for arg in args:
        url = os.path.join(url, arg)
    return url

# check index page
url = make_url()
r = requests.get(url)
assert r.status_code == 200
assert 'api' in r.json().keys()
assert 'statistics' in r.json().keys()
# check status of service
url = make_url('status')
r = requests.get(url)
enabled = r.json()['enabled']
assert isinstance(enabled, bool)
# toggle status
url = make_url('status')
data = dict(enabled=not enabled)
r = requests.post(url, json=data)
assert r.status_code == 200
# turn status off
url = make_url('status')
data = dict(enabled=True)
r = requests.post(url, json=data)
assert r.status_code == 200
assert r.json()['enabled'] is True
# make sure an empty request errors out
url = make_url('queue')
r = requests.post(url)
assert r.status_code == 422
assert 'error' in r.json().keys()
# post a url to the celery queue
url = make_url('queue')
data = dict(url='https://www.npr.org/sections/politics')
r = requests.post(url, json=data)
# report back as if aborted

# check queue to see if its there

# turn status on

# start service from standstill

# post content

# see if content shows up

print('OK')
