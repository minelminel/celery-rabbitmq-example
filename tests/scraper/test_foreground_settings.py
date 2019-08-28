import pytest
from . import app

def test_is_using_testing_config(app):
    import artifice.scraper.config.settings as settings

    assert app.config.get('TESTING') is True
    assert app.config.get('SQLALCHEMY_DATABASE_URI') is not settings.SQLALCHEMY_DATABASE_URI
