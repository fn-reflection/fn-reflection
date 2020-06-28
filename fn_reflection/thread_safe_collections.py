from collections import defaultdict, deque
from threading import Lock


class ObservedValue:
    def __init__(self, value=None):
        super().__setattr__('_lock', Lock())
        self._value = value
        self.value_setter_callbacks = []

    def __setattr__(self, name, value):
        with super().__getattribute__('_lock'):
            super().__setattr__(name, value)

    def __getattribute__(self, name):
        with super().__getattribute__('_lock'):
            return super().__getattribute__(name)

    @property
    def value(self):
        return super().__getattribute__('_value')

    @value.setter
    def value(self, value):
        super().__setattr__('_value', value)
        for callback in super().__getattribute__('_value_setter_callbacks'):
            callback(value)

    @property
    def value_setter_callbacks(self):
        return super().__getattribute__('_value_setter_callbacks')

    @value_setter_callbacks.setter
    def value_setter_callbacks(self, value_setter_callbacks):
        super().__setattr__('_value_setter_callbacks', value_setter_callbacks)


class ObservedDict(dict):
    def __init__(self, *args, **kwargs):
        self._lock = Lock()
        self.setitem_callbacks = []
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        with self._lock:
            super().__setitem__(key, value)
        for callback in self.setitem_callbacks:
            callback(self, key, value)


class ObservedDefaultDict(defaultdict):
    def __init__(self, default_factory, *args, **kwargs):
        self._lock = Lock()
        self.setitem_callbacks = []
        super().__init__(default_factory, *args, **kwargs)

    def __setitem__(self, key, value):
        with self._lock:
            super().__setitem__(key, value)
        for callback in self.setitem_callbacks:
            callback(self, key, value)


class ObservedDeque(deque):
    def __init__(self, maxlen, iterable=None):
        self._lock = Lock()
        self.append_callbacks = []
        self.appendleft_callbacks = []
        if iterable is None:
            super().__init__(maxlen=maxlen)
        else:
            super().__init__(iterable, maxlen)

    def append(self, x):
        with self._lock:
            super().append(x)
        for callback in self.append_callbacks:
            callback(self, x)

    def appendleft(self, x):
        with self._lock:
            super().appendleft(x)
        for callback in self.appendleft_callbacks:
            callback(self, x)
