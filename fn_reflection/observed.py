from typing import List, Callable, Any


class Observed:
    def __init__(self, value: Any = None, callbacks: List[Callable[[Any], Any]] = None):
        self._v: Any = value
        self._cbs: List[Callable[[Any], Any]] = callbacks if callbacks else []

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value: Any):
        self._v = value
        for c in self._cbs:
            c(self._v)

    @property
    def cbs(self):
        return self._cbs

    @cbs.setter
    def cbs(self, callbacks):
        self._cbs = callbacks
