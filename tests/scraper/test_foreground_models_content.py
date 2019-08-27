import pytest
from . import session

good_raw_data = {
  'title': 'Politics : NPR',
  'text': 'Greenland, a Danish territory, has strategic value in terms of military activity and natural resources.',
  'captions': '',
  'origin': 'https://www.npr.org/sections/politics/'
}
bad_raw_data = {
  'title': 'Politics : NPR',
  'text': 'Greenland, a Danish territory, has strategic value in terms of military activity and natural resources, said a member of Denmarks parliament.',
  'captions': '',
}
good_native_data = {
  'title': 'Politics : NPR',
  'text': 'Greenland, a Danish territory, has strategic value in terms of military activity and natural resources.',
  'captions': ['caption','here'],
  'origin': 'https://www.npr.org/sections/politics/'
}
bad_native_data = {
  'title': 'Politics : NPR',
  'text': 'Greenland, a Danish territory, has strategic value in terms of military activity and natural resources, said a member of Denmarks parliament.',
  'captions': ['caption','here'],
}
more_native_data = {
  'title': 'Sports : NPR',
  'text': 'This is some text that might be found within the page.',
  'captions': ['more','captions'],
  'origin': 'https://www.npr.org/sections/sports/'
}

def test_models_content_is_empty(session):
    from artifice.scraper.foreground.models import Content
    result = session.query(Content).all()
    assert not result

def test_models_content_add_dict_pass(session):
    from artifice.scraper.foreground.models import Content
    cls = Content(**good_raw_data)
    session.add(cls)
    session.commit()
    assert cls.id is 1

def test_models_content_add_dict_fail(session):
    from artifice.scraper.foreground.models import Content
    with pytest.raises(Exception):
        cls = Content(**bad_raw_data)
        session.add(cls)
        session.commit()

def test_models_content_add_dict_twice(session):
    from artifice.scraper.foreground.models import Content
    cls = Content(**good_raw_data)
    session.add(cls)
    session.commit()
    assert cls.id is 1
    with pytest.raises(Exception):
        cls = Content(**good_raw_data)
        session.add(cls)
        session.commit()

def test_models_content_add_cls_pass(session):
    from artifice.scraper.foreground.schemas import ContentSchema
    schema = ContentSchema()
    cls, errors = schema.load(good_native_data)
    assert not errors
    session.add(cls)
    session.commit()
    assert cls.id is 1

def test_models_content_add_cls_fail(session):
    from artifice.scraper.foreground.schemas import ContentSchema
    schema = ContentSchema()
    cls, errors = schema.load(bad_native_data)
    assert errors
    with pytest.raises(Exception):
        session.add(cls)
        session.commit()

def test_models_content_add_cls_twice(session):
    from artifice.scraper.foreground.schemas import ContentSchema
    schema = ContentSchema()
    cls, errors = schema.load(good_native_data)
    assert not errors
    session.add(cls)
    session.commit()
    assert cls.id is 1
    with pytest.raises(Exception):
        cls, errors = schema.load(good_native_data)
        assert not errors
        session.add(cls)
        session.commit()

def test_models_content_get_one(session):
    from artifice.scraper.foreground.schemas import ContentSchema
    schema = ContentSchema()
    cls, errors = schema.load(good_native_data)
    assert not errors
    session.add(cls)
    session.commit()
    data, errors = schema.dump(cls)
    assert not errors
    assert [data[key]==good_native_data[key] for key in good_native_data.keys()]

def test_models_content_get_many(session):
    from artifice.scraper.foreground.schemas import ContentSchema
    from artifice.scraper.foreground.models import Content
    schema = ContentSchema()
    cls, errors = schema.load(good_native_data)
    assert not errors
    session.add(cls)
    session.commit()
    cls, errors = schema.load(more_native_data)
    assert not errors
    session.add(cls)
    session.commit()
    schemas = ContentSchema(many=True)
    result = session.query(Content).all()
    data, errors = schemas.dump(result)
    assert not errors
    assert isinstance(data, list)
    assert len(data) is 2
