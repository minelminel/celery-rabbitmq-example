import os
import pytest
# from alembic.command import upgrade
# from alembic.config import Config

from artifice.scraper.foreground import create_app
from artifice.scraper.foreground.models import db as _db


TEST_BASE_DIR = os.getcwd()
TESTDB = 'test_project.db'
TESTDB_PATH = os.path.join(TEST_BASE_DIR, TESTDB)
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH
# ALEMBIC_CONFIG = '/opt/artifice/alembic.ini'


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    }
    app = create_app(__name__, **settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


# def apply_migrations():
#     """Applies all alembic migrations."""
#     config = Config(ALEMBIC_CONFIG)
#     upgrade(config, 'head')


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TESTDB_PATH)

    _db.app = app
    # apply_migrations()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def client(app, request):
    client = app.test_client()
    yield client


def test_is_using_testing_config(client):
    rv = client.get('/testing')
    assert rv.status_code is 200
    assert rv.json.get('TESTING') is True


# def test_api_model_content_post(session):
#     from artifice.scraper.foreground.models import Content
#     post = Content()
#     session.add(post)
#     session.commit()
#     assert post.id > 0
