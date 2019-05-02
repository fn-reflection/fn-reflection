__all__ = ['SimpleCounter']



class SimpleCounter:
    def __init__(self, initial: int = 0):
        self.c = initial

    def inc(self):
        self.c += 1

    def dec(self):
        self.c -= 1

    @property
    def count(self):
        return self.c

    def set(self, value: int):
        self.c = value
