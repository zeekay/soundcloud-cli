import sys


class InvalidSettings(Exception):
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg)

    def __str__(self):
        return self.msg

    __repr__ = __str__


class Settings(object):
    def __init__(self, filename='~/.sc'):
        import os
        self.filename = os.path.expanduser(filename)
        self.settings = None
        self.load()

    def load(self):
        import json
        import os

        self.settings = {
            'user': {},
            'users': {},
            'defaults': {}
        }

        if not os.path.exists(self.filename):
            return

        with open(self.filename) as f:
            try:
                for k,v in json.load(f).iteritems():
                    self.settings[k] = v
            except ValueError:
                raise InvalidSettings('Settings file is corrupt or missing')

    def save(self):
        import json

        with open(self.filename, 'w') as f:
            json.dump(self.settings, f)

    def __getattr__(self, name):
        if name == '_attrs' or name in self._attrs:
            raise AttributeError()

        return self.settings.get(name, None)

    def __setattr__(self, name, value):
        if name == '_attrs' or name in self._attrs:
            return super(self.Settings, self).__setattr__(name, value)

        self.settings[name] = value

Settings._attrs = set(dir(Settings) + ['Settings', 'filename', 'settings'])
Settings.InvalidSettings = InvalidSettings
Settings.Settings = Settings

sys.modules[__name__] = Settings()
