import sys


class Wrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getattr__(self, name):
        try:
            return getattr(self.wrapped, name)
        except AttributeError:
            mod = __import__(__name__ + '.' + name)
            return mod

sys.modules[__name__] = Wrapper(sys.modules[__name__])
