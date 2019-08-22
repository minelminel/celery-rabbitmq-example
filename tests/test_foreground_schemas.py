import pytest

from artifice.scraper.foreground.schemas import *


'''
~/resources/status.py

1. LOAD on request.get_json(), passed to Supervisor.toggle_status()
2. TODO: DUMP within Supervisor.status()

'''
def test_app_status_schema_good():
    schema = status_schema
    # LOAD
    stuff = {
        'enabled':True,
        'debug':False,
        'polite':1,
    }
    data, errors = schema.load(stuff)
    assert not errors
    assert stuff == data

def test_app_status_schema_okay():
    schema = status_schema
    stuff = {
        'enabled':True,
    }
    data, errors = schema.load(stuff)
    assert not errors
    assert stuff.keys() == data.keys()

def test_app_status_schema_bad():
    schema = status_schema
    stuff = {
        'enabled':4,
        'polite':0,
    }
    data, errors = schema.load(stuff)
    assert errors

def test_app_status_schema_stuff():
    schema = status_schema
    stuff = {
        'pizza':4,
        'bagel':[6,'9'],
    }
    data, errors = schema.load(stuff)
    assert not errors
    assert not data


'''
~/resources/queue.py

1. DUMP with request.args via GET
'''
def test_app_queue_args_schema_good():
    schema = queue_args_schema
    stuff = {
        'status':'READY',
        'limit':123,
    }
    params, errors = schema.dump(stuff)
    assert not errors
    assert stuff.get('limit') == params.get('limit')

def test_app_queue_args_schema_okay():
    schema = queue_args_schema
    stuff = {
        'limit':0,
    }
    params, errors = schema.dump(stuff)
    assert not errors
    assert stuff.get('limit') == params.get('limit')

def test_app_queue_args_schema_bad():
    schema = queue_args_schema
    stuff = {
        'status':['ready','mistake'],
    }
    params, errors = schema.dump(stuff)
    assert errors is not None


# def test_app_queues_schema():
#     # queues_schema
#     schema = queues_schema
#     pass
#
#
# def test_queue_task_schema():
#     # queue_task_schema
#     schema = queue_task_schema
#     pass
#
#
# def test_queue_tasks_schema():
#     # queues_task_schema
#     schema = queues_task_schema
#     pass
#
#
# def test_app_content_schema():
#     # content_schema
#     schema = content_schema
#     pass
#
#
# def test_app_contents_schema():
#     # content_schema
#     schema = content_schema
#     pass
#
#
# def test_app_args_schema():
#     # args_schema
#     schema = args_schema
#     pass
#
# def test_app_queue_args_schema():
#     # queue_args_schema
#     schema = queue_args_schema
#     pass
