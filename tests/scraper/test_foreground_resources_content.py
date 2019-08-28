import pytest
from . import client
from . import post_json, de_json


# def test_foreground_resources_content_get(client):
#     rv = client.get('/content')
#     assert rv.status_code == 200
#     assert 'msg' in rv.json.keys()
#     assert 'reply' in rv.json.keys()
