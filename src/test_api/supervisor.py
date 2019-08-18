import datetime

class Supervisor:
    def __init__(self, enabled=False, debug=False):
        self.enabled = enabled
        self.debug = debug
        self.time = datetime.datetime.now()

    def status(self):
        return dict(enabled=self.enabled,debug=self.debug)

    def _enable(self):
        if not self.enabled:
            self.enabled = True

    def _disable(self):
        if self.enabled:
            self.enabled = False

    def debug_on(self):
        if not self.debug:
            self.debug = True

    def debug_off(self):
        if self.debug:
            self.debug = False

    def toggle_status(self, data):
        if data.get('enabled') is True:
            self._enable()
        elif data.get('enabled') is False:
            self._disable()
        if data.get('debug') is True:
            self.debug_on()
        elif data.get('debug') is False:
            self.debug_off()

    def uptime(self):
        td = str(datetime.datetime.now() - self.time)
        return td.split('.')[0]
