import pytest
from . import session


def test_models_queue_is_empty(session):
    '''
    ensure that a fresh database is present
    '''
    from artifice.scraper.foreground.models import Queue
    result = session.query(Queue).all()
    assert not result

def test_models_queue_add_one_pass(session):
    '''
    add a single url in a raw format without use of schemas
    '''
    from artifice.scraper.foreground.models import Queue
    data = {'url': 'https://www.npr.org/sections/politics/'}
    cls = Queue(**data)
    session.add(cls)
    session.commit()
    assert cls.id is 1
    assert cls.status == 'READY'

def test_models_queue_add_one_fail(session):
    '''
    ensure exception is raised if no valid keys are present
    '''
    from artifice.scraper.foreground.models import Queue
    data = {'malicious': 'goo goo ga ga'}
    with pytest.raises(Exception):
        cls = Queue(**data)
        session.add(cls)
        session.commit()

def test_models_queue_add_same_twice(session):
    '''
    ensure exception is raised if the entry exists
    '''
    from artifice.scraper.foreground.models import Queue
    data = {'url': 'https://www.npr.org/sections/politics/'}
    cls = Queue(**data)
    session.add(cls)
    session.commit()
    assert cls.id is 1
    with pytest.raises(Exception):
        cls = Queue(**data)
        session.add(cls)
        session.commit()

def test_models_queue_status_override(session):
    '''
    ensure that status can be overridden by data
    '''
    from artifice.scraper.foreground.schemas import QueueSchema
    schema = QueueSchema()
    data = {'url':'https://www.npr.org/sections/politics/',
            'status':'DONE'}
    cls, errors = schema.load(data)
    assert not errors
    session.add(cls)
    session.commit()
    assert cls.status == 'DONE'

# def test_models_queue_get_one(session):
#     from artifice.scraper.foreground.schemas import QueueSchema
#     schema = QueueSchema()
#     schemas = QueueSchema(many=True)
#     data =
#     cls, errors = schema.load(data)
#     assert not errors
#     session.add(cls)
#     session.commit()
#     data, errors = schema.dump(cls)
#     assert not errors
#     assert [data[key]==good_native_data[key] for key in good_native_data.keys()]
#
# def test_models_queue_get_many(session):
#     from artifice.scraper.foreground.schemas import QueueSchema
#     from artifice.scraper.foreground.models import Queue
#     schema = QueueSchema()
#     cls, errors = schema.load(good_native_data)
#     assert not errors
#     session.add(cls)
#     session.commit()
#     cls, errors = schema.load(more_native_data)
#     assert not errors
#     session.add(cls)
#     session.commit()
#     schemas = QueueSchema(many=True)
#     result = session.query(Queue).all()
#     data, errors = schemas.dump(result)
#     assert not errors
#     assert isinstance(data, list)
#     assert len(data) is 2
