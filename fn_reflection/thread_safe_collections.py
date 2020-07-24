from collections import deque
from collections.abc import MutableMapping
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


class ObservedDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self._lock = Lock()
        self.setitem_callbacks = []
        self.update_callbacks = []
        self.store.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        with self._lock:
            return self.store[key]

    def get(self, key, default=None):
        with self._lock:
            return self.store.get(key, default)

    def __setitem__(self, key, value):
        with self._lock:
            self.store[key] = value
            for callback in self.setitem_callbacks:
                callback(self.store, {key: value})

    def __delitem__(self, key):
        with self._lock:
            del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        with self._lock:
            return len(self.store)

    def __repr__(self):
        return repr(self.store)

    def __str__(self):
        return str(self.store)

    def update(self, m=None, **kwargs):
        with self._lock:
            if m is not None:
                self.store.update(m, **kwargs)
            else:
                self.store.update(**kwargs)
            for callback in self.update_callbacks:
                d = dict(m, **kwargs) if m is not None else kwargs
                callback(self.store, d)


class ObservedDefaultDict(MutableMapping):
    def __init__(self, default_factory, **kwargs):
        self.store = dict()
        self._lock = Lock()
        self.default_factory = default_factory
        self.setitem_callbacks = []
        self.update_callbacks = []
        self.store.update(**kwargs)

    def __getitem__(self, key):
        with self._lock:
            value = self.store.get(key)
            if value:
                return value
            default = self.default_factory()
            self.store[key] = default
            return default

    def get(self, key, default=None):
        with self._lock:
            return self.store.get(key, default)

    def __setitem__(self, key, value):
        with self._lock:
            self.store[key] = value
            for callback in self.setitem_callbacks:
                callback(self.store, {key: value})

    def __delitem__(self, key):
        with self._lock:
            del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        with self._lock:
            return len(self.store)

    def __repr__(self):
        return repr(self.store)

    def __str__(self):
        return str(self.store)

    def update(self, m=None, **kwargs):
        with self._lock:
            if m is not None:
                self.store.update(m, **kwargs)
            else:
                self.store.update(**kwargs)
            for callback in self.update_callbacks:
                d = dict(m, **kwargs) if m is not None else kwargs
                callback(self.store, d)


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
