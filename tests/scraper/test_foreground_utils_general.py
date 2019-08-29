import pytest


def test_app__side_load():
    from artifice.scraper.foreground.utils.general import _side_load
    key = 'ABC'
    data = {key:[1,2,3]}
    reply = _side_load(data)
    assert reply == [{key:1},{key:2},{key:3}]

def test_app_side_load_list():
    from artifice.scraper.foreground.utils.general import side_load
    data1 = {'ABC':[1,2,3]}
    data2 = {'XYZ':'hello'}
    data3 = {42:'world'}
    data = {**data1,**data2,**data3}
    key = 'ABC'
    reply = side_load(key, data)
    assert reply == [{key:1},{key:2},{key:3}]

def test_app_side_load_string():
    from artifice.scraper.foreground.utils.general import side_load
    data1 = {'ABC':[1,2,3]}
    data2 = {'XYZ':'hello'}
    data3 = {42:'world'}
    data = {**data1,**data2,**data3}
    key = 'XYZ'
    reply = side_load(key, data)
    assert reply == [{key:'hello'}]

def test_app_setattrs():
    from artifice.scraper.foreground.utils.general import setattrs
    class Obj:
        age = 25
        name = 'Bob'
        weight = 165
    obj = Obj()
    assert obj.age == 25
    assert obj.name == 'Bob'
    assert obj.weight == 165
    setattrs(obj, age=10, name='Billy', weight=210)
    assert obj.age == 10
    assert obj.name == 'Billy'
    assert obj.weight == 210

def test_app_cmp_dict():
    from artifice.scraper.foreground.utils.general import cmp_dict
    before = {'A':1,'B':2,'C':3}
    after = {'A':1,'B':22,'C':33}
    reply = cmp_dict(before, after)
    assert reply == {'B':22,'C':33}

    before = {'A':1,'B':2,'C':3}
    after = {'A':1,'B':2,'C':3}
    reply = cmp_dict(before, after)
    assert not reply
