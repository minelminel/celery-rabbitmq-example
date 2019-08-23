import pytest
from flask import request


@pytest.fixture
def server():
    import flask
    app = flask.Flask(__name__)
    from artifice.scraper.foreground.utils.decorators import requires_body
    @app.route('/requires_body')
    @requires_body
    def index():
        return 'OK', 200

    server = app.test_client()
    yield server


def test_app_requires_body(server):
    rv = server.get('/requires_body')
    assert rv.status_code == 422
    assert rv.json.get('error') == 'Request body cannot be empty'
