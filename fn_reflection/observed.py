from typing import List, Callable, Any


class Observed:
    def __init__(self, value: Any = None, callbacks: List[Callable[[Any], Any]] = None):
        self._v: Any = value
        self._callbacks: List[Callable[[Any], Any]] = callbacks if callbacks else []

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value: Any):
        self._v = value
        for c in self._callbacks:
            c(self._v)

    @property
    def callbacks(self):
        return self._callbacks

    @callbacks.setter
    def callbacks(self, callbacks):
        self._callbacks = callbacks
