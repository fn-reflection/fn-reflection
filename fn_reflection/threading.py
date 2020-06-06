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


class ObservedWithLock:
    def __init__(self, data: Any = None, callbacks: List[Callable[[Any], Any]] = None):
        super().__setattr__('_lock', Lock())
        self._data: Any = data
        self._callbacks: List[Callable[[Any], Any]
                              ] = callbacks if callbacks else []

    def __setattr__(self, name, data):
        with super().__getattribute__('_lock'):
            super().__setattr__(name, data)

    def __getattribute__(self, name):
        with super().__getattribute__('_lock'):
            return super().__getattribute__(name)

    @property
    def data(self):
        return super().__getattribute__('_data')

    @data.setter
    def data(self, value: Any):
        super().__setattr__('_data', value)
        for c in super().__getattribute__('_callbacks'):
            c(super().__getattribute__('_data'))

    @property
    def callbacks(self):
        return super().__getattribute__('_callbacks')

    @callbacks.setter
    def callbacks(self, callbacks):
        super().__setattr__('_callbacks', callbacks)
