import pytest
from . import *

def test_models_is_using_testing_config(app):
    from artifice.scraper.foreground.config import Config
    assert app.config.get('TESTING') is True
    assert app.config.get('SQLALCHEMY_DATABASE_URI') is not Config.SQLALCHEMY_DATABASE_URI

def test_models_content_is_empty(session):
    from artifice.scraper.foreground.models import Content
    result = session.query(Content).all()
    assert not result

def test_models_content_add_dict_pass(session):
    from artifice.scraper.foreground.models import Content
    data = {
      'title': 'Politics : NPR',
      'text': 'Greenland, a Danish territory, has strategic value in terms of military activity and natural resources.',
      'captions': '',
      'origin': 'https://www.npr.org/sections/politics/'
    }
    cls = Content(**data)
    session.add(cls)
    session.commit()
    assert cls.id > 0

def test_models_content_add_dict_fail(session):
    from artifice.scraper.foreground.models import Content
    import sqlalchemy
    data = {
      'title': 'Politics : NPR',
      'text': 'Greenland, a Danish territory, has strategic value in terms of military activity and natural resources, said a member of Denmarks parliament. AP hide caption August 16, 2019 • NPR thanks our sponsors Become an NPR sponsor',
      'captions': '',
    }
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        cls = Content(**data)
        session.add(cls)
        session.commit()

def test_models_content_add_dict_twice(session):
    from artifice.scraper.foreground.models import Content
    import sqlalchemy
    data = {
      'title': 'Politics : NPR',
      'text': 'Greenland, a Danish territory, has strategic value in terms of military activity and natural resources.',
      'captions': '',
      'origin': 'https://www.npr.org/sections/politics/'
    }
    cls = Content(**data)
    session.add(cls)
    session.commit()
    assert cls.id > 0
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        cls = Content(**data)
        session.add(cls)
        session.commit()
