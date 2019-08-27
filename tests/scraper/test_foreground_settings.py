import pytest
from . import app

def test_is_using_testing_config(app):
    from artifice.scraper.foreground.config import Config
    assert app.config.get('TESTING') is True
    assert app.config.get('SQLALCHEMY_DATABASE_URI') is not Config.SQLALCHEMY_DATABASE_URI
