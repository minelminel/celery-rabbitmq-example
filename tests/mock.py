import unittest
import os
import time
import requests

seed_url = 'https://www.npr.org/sections/politics'

def make_url(*args):
    url = 'http://localhost:8080'
    for arg in args:
        url = os.path.join(url, arg)
    return url

# check index page
print('[check index page]')
url = make_url()
r = requests.get(url)
assert r.status_code == 200
assert 'api' in r.json().keys()
assert 'statistics' in r.json().keys()
# check status of service
print('[check if enabled]')
url = make_url('status')
r = requests.get(url)
enabled = r.json()['enabled']
assert isinstance(enabled, bool)
# toggle status
print('[toggle status]')
url = make_url('status')
data = dict(enabled=not enabled)
r = requests.post(url, json=data)
assert r.status_code == 200
# turn status off
print('[disable service]')
url = make_url('status')
data = dict(enabled=True)
r = requests.post(url, json=data)
assert r.status_code == 200
assert r.json()['enabled'] is True
# make sure an empty request errors out
print('[ensure empty QUEUE POST throws error]')
url = make_url('queue')
r = requests.post(url)
assert r.status_code == 422
assert 'error' in r.json().keys()
# turn debug mode on
print('turning task debug mode ON')
url = make_url('status')
data = dict(debug=True)
r = requests.post(url, json=data)
assert r.status_code == 200
assert r.json()['debug'] is True
# post a url to the celery queue
print('[post task to celery queue]')
url = make_url('queue')
data = dict(url=seed_url)
r = requests.post(url, json=data)
assert r.status_code == 200
# report back as if aborted
print('[simulating disabled service url return]')
url = make_url('queue')
data = dict(url=seed_url,status='READY')
r = requests.put(url, json=data)
assert r.status_code == 200
assert r.json()['status'] == 'READY'
# check queue to see if its there
print('[checking queue for seed_url]')
url = make_url('queue')
r = requests.get(url)
assert r.status_code == 200
assert r.json()['response'][0]['status'] == 'READY'
# start service from standstill
print('[starting service from standstill]')
url = make_url('status')
r = requests.put(url)
assert r.status_code == 200
# return url as DONE
url = make_url('queue')
data = dict(url=seed_url,status='DONE')
r = requests.put(url, json=data)
assert r.status_code == 200
assert r.json()['status'] == 'DONE'
# post content
print('[posting content]')
url = make_url('content')
data = dict(
    origin=seed_url,
    title='hello, world!',
    text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    captions=[],
    url=[seed_url],
)
r = requests.post(url, json=data)
assert r.status_code == 200
# see if content shows up
print('[checking content]')
url = make_url('content')
del data['url']
r = requests.get(url)
assert r.status_code == 200
assert r.json()['reply']

print('\n\tOK!')
