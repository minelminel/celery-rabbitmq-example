from .conftest import app, db, session, client
from .conftools import post_json, de_json
# import os
# import tempfile
# import pytest
#
# from artifice.scraper.foreground import create_app
#
#
# @pytest.fixture
# def client():
#     app = create_app()
#     db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#     app.config['TESTING'] = True
#     client = app.test_client()
#
#     yield client
#
#     os.close(db_fd)
#     os.unlink(app.config['DATABASE'])
