import pytest
from . import client
from . import post_json, de_json


def test_foreground_resources_status_get_enabled(client):
    rv = client.get('/status')
    assert rv.status_code == 200
    assert type(rv.json['enabled']) is bool
    assert type(rv.json['debug']) is bool
    assert type(rv.json['polite']) is (int or float)
    assert type(rv.json['msg']) is list

def test_foreground_resources_enabled_toggle(client):
    url = '/status'
    data = {'enabled':True}
    response = post_json(client, url, data)
    assert response.status_code == 200
    jsn = de_json(response)
    assert jsn.get('enabled') == data.get('enabled')
    data = {'enabled':False}
    response = post_json(client, url, data)
    assert response.status_code == 200
    jsn = de_json(response)
    assert jsn.get('enabled') == data.get('enabled')

def test_foreground_resources_debug_toggle(client):
    url = '/status'
    data = {'debug':True}
    response = post_json(client, url, data)
    assert response.status_code == 200
    jsn = de_json(response)
    assert jsn.get('debug') == data.get('debug')
    data = {'debug':False}
    response = post_json(client, url, data)
    assert response.status_code == 200
    jsn = de_json(response)
    assert jsn.get('debug') == data.get('debug')

def test_foreground_resources_polite_toggle(client):
    url = '/status'
    data = {'polite':2}
    response = post_json(client, url, data)
    assert response.status_code == 200
    jsn = de_json(response)
    assert jsn.get('polite') == data.get('polite')
    data = {'polite':3.14}
    response = post_json(client, url, data)
    jsn = de_json(response)
    assert jsn.get('polite') == data.get('polite')

def test_foreground_resources_toggle_many(client):
    url = '/status'
    data = {'enabled':True,'debug':False,'polite':2}
    response = post_json(client, url, data)
    assert response.status_code == 200
    jsn = de_json(response)
    assert jsn.get('polite') == data.get('polite')
    data = {'enabled':False,'debug':True,'polite':1.5}
    response = post_json(client, url, data)
    assert response.status_code == 200
    jsn = de_json(response)
    assert jsn.get('polite') == data.get('polite')

# def test_foreground_resources_toggle_fail(client):
#     url = 'status'
#     data = {'foo':'bar',3:['c','o','w'],'!@#$%':None}
#     response = post_json(client, url, data)
#     assert not response.__dict__
#     # assert response.status_code == 422
