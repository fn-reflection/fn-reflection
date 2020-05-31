from typing import List, Callable, Any
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


class ObservedWithLock(WithLock):
    def __init__(self, data: Any = None, callbacks: List[Callable[[Any], Any]] = None):
        super().__init__()
        cbs = callbacks if callbacks else []
        self._data: Any = data
        self._callbacks: List[Callable[[Any], Any]] = cbs

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: Any):
        self._data = value
        for c in self._callbacks:
            c(self._data)

    @property
    def callbacks(self):
        return self._callbacks

    @callbacks.setter
    def callbacks(self, callbacks):
        self._callbacks = callbacks
