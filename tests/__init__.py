import os
import tempfile
import pytest

from artifice.scraper.foreground import create_app


@pytest.fixture
def client(request):
    app = create_app()
    # settings_override = {
    #     'TESTING': True,
    #     'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    # }
    # app = create_app(__name__, settings_override)
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
