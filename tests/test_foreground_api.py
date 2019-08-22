import pytest
from . import client
# GET requests, atomic operations

def test_app_index_get(client):
    '''
    ensure index route is active and that
    routes were successfully registered
    '''
    rv = client.get('/')
    assert isinstance(rv.json, list)
    assert len(rv.json) > 0


def test_app_status_get_debug(client):
    '''
    ensure status route is returning a valid DEBUG value
    '''
    rv = client.get('/status')
    key = 'debug'
    val = rv.json.get(key)
    assert isinstance(val, bool)


def test_app_status_get_enabled(client):
    '''
    ensure status route is returning a valid ENABLED value
    '''
    rv = client.get('/status')
    key = 'enabled'
    val = rv.json.get(key)
    assert isinstance(val, bool)


def test_app_status_get_msg(client):
    '''
    ensure status route is returning a valid MSG value
    '''
    rv = client.get('/status')
    key = 'msg'
    val = rv.json.get(key)
    assert isinstance(val, list)


def test_app_status_get_polite(client):
    '''
    ensure status route is returning a valid polite value
    '''
    rv = client.get('/status')
    key = 'polite'
    val = rv.json.get(key)
    assert isinstance(val, (int, float))
    assert val > 0


def test_app_stats_get_database(client):
    '''
    ensure stat route displays our database sizes
    and that all values are integers
    '''
    rv = client.get('/stats')
    key = 'database'
    assert 'Content','Queue' in rv.json.get(key).keys()
    for each, data in rv.json.get(key).items():
        for val in data.values():
            assert isinstance(val, int)


def test_app_stats_get_service(client):
    '''
    ensure stat route displays our service statistics
    '''
    rv = client.get('/stats')
    key = 'service'
    assert rv.json.get(key) is not None
    reqs = rv.json.get(key).get('requests')
    assert isinstance(reqs, int)
    rpm = rv.json.get(key).get('rpm')
    assert isinstance(rpm, int)
    uptime = rv.json.get(key).get('uptime')
    assert isinstance(uptime, str)


def test_app_queue_get(client):
    '''
    ensure queue route displays the proper formatting.
    no args are passed so test for default values.
    '''
    rv = client.get('/queue')
    msg = rv.json.get('msg')
    assert 'limit' in msg.keys()
    assert 'status' in msg.keys()
    assert isinstance(msg.get('status'), list)
    reply = rv.json.get('reply')
    assert isinstance(reply, list)


def test_app_content_get(client):
    '''
    ensure content route displays the proper formatting.
    no args are passed so test for default values.
    '''
    rv = client.get('/queue')
    msg = rv.json.get('msg')
    assert 'limit' in msg.keys()
    reply = rv.json.get('reply')
    assert isinstance(reply, list)
