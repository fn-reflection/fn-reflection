from threading import Lock


class WithLock:
    def __init__(self, **kwargs):
        super().__setattr__('_lock', Lock())
        for k, v in kwargs.items():
            super().__setattr__(k, v)

    def __setattr__(self, name, data):
        with super().__getattribute__('_lock'):
            super().__setattr__(name, data)

    def __getattribute__(self, name):
        with super().__getattribute__('_lock'):
            return super().__getattribute__(name)
