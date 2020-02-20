import operator
import itertools
from typing import Dict, Deque, Callable
__all__ = ['multiple_sort', 'partition_by',
           'ignore_none_dict', 'renamed_dict', 'CyclicCounter']


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


def renamed_dict(d: Dict, rename_d: Dict):
    return {key_to: d[key_from] for key_from, key_to in rename_d.items()}


class CyclicCounter:
    def __init__(self, limit: int = 1000000000):
        self.counter: int = 0
        self.limit: int = limit

    def up(self, num: int = 1):
        value = self.counter
        self.counter += num
        self.counter %= self.limit
        return value


def pop_old_elements(deque: Deque, predicate: Callable):
    old_element_count = 0
    for elem in deque:
        if predicate(elem):
            old_element_count += 1
        else:
            break
    for _ in range(old_element_count):
        deque.popleft()
