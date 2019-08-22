import datetime

from ..utils import cmp_dict

class Supervisor:
    def __init__(self, enabled=False, debug=False, politeness=1):
        self.enabled = enabled
        self.debug = debug
        self.time = datetime.datetime.now()
        self.politeness = politeness

    def uptime(self):
        td = str(datetime.datetime.now() - self.time)
        return td.split('.')[0]

    def status(self):
        return dict(
            enabled=self.enabled,
            debug=self.debug,
            politeness=self.politeness
        )

    def _enable(self):
        if not self.enabled:
            self.enabled = True

    def _disable(self):
        if self.enabled:
            self.enabled = False

    def _debug_on(self):
        if not self.debug:
            self.debug = True

    def _debug_off(self):
        if self.debug:
            self.debug = False

    def _toggle_enabled(self, data):
        if data.get('enabled') is True:
            self._enable()
        elif data.get('enabled') is False:
            self._disable()

    def _toggle_debug(self, data):
        if data.get('debug') is True:
            self._debug_on()
        elif data.get('debug') is False:
            self._debug_off()

    def _toggle_politeness(self, data):
        new_value = data.get('politeness')
        if isinstance(new_value, bool):
            pass
        elif isinstance(new_value, (int, float)):
            self.politeness = new_value

    def toggle_status(self, data):
        before = self.status()
        self._toggle_enabled(data)
        self._toggle_debug(data)
        self._toggle_politeness(data)
        after = self.status()
        changed = cmp_dict(before, after)
        return changed

    @staticmethod
    def render_msg(data):
        reply = []
        if not data:
            return reply
        for k, v in data.items():
            reply.append('{} ==> {}'.format(k, v))
        return reply
