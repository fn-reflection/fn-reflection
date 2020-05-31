from typing import List, Callable, Any


class Observed:
    def __init__(self, data: Any = None, callbacks: List[Callable[[Any], Any]] = None):
        self._data: Any = data
        self._callbacks: List[Callable[[Any], Any]] = callbacks if callbacks else []

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: Any):
        self._data = data
        for c in self._callbacks:
            c(self._data)

    @property
    def callbacks(self):
        return self._callbacks

    @callbacks.setter
    def callbacks(self, callbacks):
        self._callbacks = callbacks
