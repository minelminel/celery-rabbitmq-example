import pytest
from . import post_json, de_json

@pytest.fixture
def server():
    import flask
    app = flask.Flask(__name__)
    from artifice.scraper.foreground.utils.decorators import requires_body
    @app.route('/requires_body', methods=['GET','POST'])
    @requires_body
    def index():
        return 'OK', 200

    server = app.test_client()
    yield server


def test_app_requires_body_fail(server):
    rv = server.get('/requires_body')
    assert rv.status_code == 422
    assert rv.json.get('error') == 'Request body cannot be empty'

def test_app_requires_body_pass(server):
    url = '/requires_body'
    data = {'data':'present','in':'request'}
    response = post_json(server, url, data)
    assert response.status_code == 200
