import os


class Supervisor:
    def __init__(self, enabled):
        self.enabled = enabled

    def status(self):
        return dict(enabled=self.enabled)

    def _enable(self):
        if not self.enabled:
            self.enabled = True

    def _disable(self):
        if self.enabled:
            self.enabled = False

    def toggle_status(self, data):
        if data.get('enabled') is True:
            self._enable()
        elif data.get('enabled') is False:
            self._disable()
