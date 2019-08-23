import pytest
import datetime

from artifice.scraper.foreground.supervisor import Supervisor


def test_supervisor_default_init_types():
    sv = Supervisor()
    assert isinstance(sv.enabled, bool)
    assert isinstance(sv.debug, bool)
    assert isinstance(sv.polite, (int, float))
    assert isinstance(sv.time, datetime.datetime)


def test_supervisor_default_init_values():
    sv = Supervisor(enabled=False, debug=False, polite=1)
    assert sv.enabled is False
    assert sv.debug is False
    assert sv.polite == 1


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
    assert 'polite' in status.keys()
    assert sv.enabled == status.get('enabled')
    assert sv.debug == status.get('debug')
    assert sv.polite == status.get('polite')


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


def test_supervisor__toggle_polite():
    sv = Supervisor(polite=1)
    assert sv.polite == 1
    sv._toggle_polite({'polite':3.14})
    assert sv.polite == 3.14
    sv._toggle_polite({'polite':0.0001})
    assert sv.polite == 0.0001
    sv._toggle_polite({'polite':2})
    assert sv.polite == 2
    sv._toggle_polite({'polite':True})
    assert sv.polite == 2
    sv._toggle_polite({'polite':'abc'})
    assert sv.polite == 2
    sv._toggle_polite({'polite':{1}})
    assert sv.polite == 2
    sv._toggle_polite({'polite':[1]})
    assert sv.polite == 2
    sv._toggle_polite({})
    assert sv.polite == 2


def test_supervisor_toggle_status():
    sv = Supervisor(enabled=False, debug=False, polite=1)

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

    ch = sv.toggle_status({'polite':1})
    assert not ch
    assert sv.polite == 1
    ch = sv.toggle_status({'polite':2})
    assert ch == {'polite':2}
    assert sv.polite == 2
    ch = sv.toggle_status({'polite':'abc'})
    assert not ch
    assert sv.polite == 2
    ch = sv.toggle_status({'polite':False})
    assert not ch
    assert sv.polite == 2
    ch = sv.toggle_status({})
    assert not ch
    assert sv.polite == 2


def test_supervisor_render_msg():
    sv = Supervisor()
    data = dict(enabled=True)
    msg = sv.render_msg(data)
    assert 'enabled ==> True' in msg
    data = dict(debug=True)
    msg = sv.render_msg(data)
    assert 'debug ==> True' in msg
    data = dict(polite=1)
    msg = sv.render_msg(data)
    assert 'polite ==> 1' in msg
    data = dict(enabled=True, debug=True, polite=1)
    msg = sv.render_msg(data)
    assert 'enabled ==> True' in msg
    assert 'debug ==> True' in msg
    assert 'polite ==> 1' in msg
    data = None
    msg = sv.render_msg(data)
    assert not msg
