import pytest
from . import client
from . import post_json, de_json


def test_foreground_resources_index_get(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert isinstance(rv.json, list)
    assert [kwarg in rv.json.pop().keys() for kwarg in ['rule','route','method']]

def test_foreground_resources_index_forbiddens(client):
    rv = client.post('/')
    assert rv.status_code == 405
    rv = client.put('/')
    assert rv.status_code == 405
    rv = client.delete('/')
    assert rv.status_code == 405
