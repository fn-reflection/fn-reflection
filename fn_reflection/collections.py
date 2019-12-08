import operator
import itertools
__all__ = ['multiple_sort', 'partition_by',
           'ignore_none_dict', 'CyclicCounter']


def partition_by(coll, f):
    flip_flop = False

    def switch(item):
        nonlocal flip_flop
        if f(item):
            flip_flop = not flip_flop
        return flip_flop
    return map(lambda grp: list(grp[1]), itertools.groupby(coll, switch))


def multiple_sort(xs, specs):
    getter = (operator.itemgetter if isinstance(specs, list) or isinstance(specs, tuple)
              else operator.attrgetter)
    for key, reverse in reversed(specs):
        xs.sort(key=getter(key), reverse=reverse)
    return xs


def ignore_none_dict(**args):
    return {k: v for k, v in args.items() if v is not None}


class CyclicCounter:
    def __init__(self, limit: int = 1000000000):
        self.counter: int = 0
        self.limit: int = limit

    def up(self, num: int = 1):
        value = self.counter
        self.counter += num
        self.counter %= self.limit
        return value
