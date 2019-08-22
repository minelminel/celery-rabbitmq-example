import pytest
import datetime

from artifice.scraper.foreground.supervisor import Supervisor


def test_supervisor_default_init_types():
    sv = Supervisor()
    assert isinstance(sv.enabled, bool)
    assert isinstance(sv.debug, bool)
    assert isinstance(sv.politeness, (int, float))
    assert isinstance(sv.time, datetime.datetime)


def test_supervisor_default_init_values():
    sv = Supervisor(enabled=False, debug=False, politeness=1)
    assert sv.enabled is False
    assert sv.debug is False
    assert sv.politeness == 1


def test_supervisor_uptime():
    sv = Supervisor()
    uptime = sv.uptime()
    assert isinstance(uptime, str)
    assert len(uptime.split(':')) == 3
    # hack to make sure that the middle element is mins, not seconds
    assert uptime.split(':')[1] == '00'


def test_supervisor_status():
    sv = Supervisor()
    status = sv.status()
    assert 'enabled' in status.keys()
    assert 'debug' in status.keys()
    assert 'politeness' in status.keys()
    assert sv.enabled == status.get('enabled')
    assert sv.debug == status.get('debug')
    assert sv.politeness == status.get('politeness')


def test_supervisor__enable():
    sv = Supervisor(enabled=False)
    assert sv.enabled is False
    sv._enable()
    assert sv.enabled is True
    sv._enable()
    assert sv.enabled is True


def test_supervisor__disable():
    sv = Supervisor(enabled=True)
    assert sv.enabled is True
    sv._disable()
    assert sv.enabled is False
    sv._disable()
    assert sv.enabled is False


def test_supervisor__debug_on():
    sv = Supervisor(debug=False)
    assert sv.debug is False
    sv._debug_on()
    assert sv.debug is True
    sv._debug_on()
    assert sv.debug is True


def test_supervisor__debug_off():
    sv = Supervisor(debug=True)
    assert sv.debug is True
    sv._debug_off()
    assert sv.debug is False
    sv._debug_off()
    assert sv.debug is False


def test_supervisor__toggle_enabled():
    sv = Supervisor(enabled=False)
    assert sv.enabled is False
    sv._toggle_enabled({'enabled':True})
    assert sv.enabled is True
    sv._toggle_enabled({'enabled':True})
    assert sv.enabled is True
    sv._toggle_enabled({'enabled':False})
    assert sv.enabled is False
    sv._toggle_enabled({'enabled':False})
    assert sv.enabled is False
    sv._toggle_enabled({})
    assert sv.enabled is False
    sv.enabled = True
    sv._toggle_enabled({})
    assert sv.enabled is True


def test_supervisor__toggle_debug():
    sv = Supervisor(debug=False)
    assert sv.debug is False
    sv._toggle_debug({'debug':True})
    assert sv.debug is True
    sv._toggle_debug({'debug':True})
    assert sv.debug is True
    sv._toggle_debug({'debug':False})
    assert sv.debug is False
    sv._toggle_debug({'debug':False})
    assert sv.debug is False
    sv._toggle_debug({})
    assert sv.debug is False
    sv.debug = True
    sv._toggle_debug({})
    assert sv.debug is True


def test_supervisor__toggle_politeness():
    sv = Supervisor(politeness=1)
    assert sv.politeness == 1
    sv._toggle_politeness({'politeness':3.14})
    assert sv.politeness == 3.14
    sv._toggle_politeness({'politeness':0.0001})
    assert sv.politeness == 0.0001
    sv._toggle_politeness({'politeness':2})
    assert sv.politeness == 2
    sv._toggle_politeness({'politeness':True})
    assert sv.politeness == 2
    sv._toggle_politeness({'politeness':'abc'})
    assert sv.politeness == 2
    sv._toggle_politeness({'politeness':{1}})
    assert sv.politeness == 2
    sv._toggle_politeness({'politeness':[1]})
    assert sv.politeness == 2
    sv._toggle_politeness({})
    assert sv.politeness == 2


def test_supervisor_toggle_status():
    sv = Supervisor(enabled=False, debug=False, politeness=1)

    ch = sv.toggle_status({'enabled':False})
    assert not ch
    assert sv.enabled is False
    ch = sv.toggle_status({'enabled':True})
    assert ch == {'enabled':True}
    assert sv.enabled is True
    ch = sv.toggle_status({'enabled':True})
    assert not ch
    assert sv.enabled is True
    ch = sv.toggle_status({'enabled':False})
    assert ch == {'enabled':False}
    assert sv.enabled is False
    ch = sv.toggle_status({})
    assert not ch
    assert sv.enabled is False

    ch = sv.toggle_status({'debug':False})
    assert not ch
    assert sv.debug is False
    ch = sv.toggle_status({'debug':True})
    assert ch == {'debug':True}
    assert sv.debug is True
    ch = sv.toggle_status({'debug':True})
    assert not ch
    assert sv.debug is True
    ch = sv.toggle_status({'debug':False})
    assert ch == {'debug':False}
    assert sv.debug is False
    ch = sv.toggle_status({})
    assert not ch
    assert sv.debug is False

    ch = sv.toggle_status({'politeness':1})
    assert not ch
    assert sv.politeness == 1
    ch = sv.toggle_status({'politeness':2})
    assert ch == {'politeness':2}
    assert sv.politeness == 2
    ch = sv.toggle_status({'politeness':'abc'})
    assert not ch
    assert sv.politeness == 2
    ch = sv.toggle_status({'politeness':False})
    assert not ch
    assert sv.politeness == 2
    ch = sv.toggle_status({})
    assert not ch
    assert sv.politeness == 2


def test_supervisor_render_msg():
    sv = Supervisor()
    data = dict(enabled=True)
    msg = sv.render_msg(data)
    assert 'enabled ==> True' in msg
    data = dict(debug=True)
    msg = sv.render_msg(data)
    assert 'debug ==> True' in msg
    data = dict(politeness=1)
    msg = sv.render_msg(data)
    assert 'politeness ==> 1' in msg
    data = dict(enabled=True, debug=True, politeness=1)
    msg = sv.render_msg(data)
    assert 'enabled ==> True' in msg
    assert 'debug ==> True' in msg
    assert 'politeness ==> 1' in msg
