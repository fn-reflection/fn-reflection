import operator
import itertools
__all__ = ['multiple_sort',  'partition_by']


def partition_by(coll, f):
    flip_flop = False

    def switch(item):
        nonlocal flip_flop
        if f(item):
            flip_flop = not flip_flop
        return flip_flop
    return map(lambda grp: list(grp[1]), itertools.groupby(coll, switch))


def multiple_sort(xs, specs):
    if isinstance(specs, list) or isinstance(specs, tuple):
        getter = operator.itemgetter
    else:
        getter = operator.attrgetter
    for key, reverse in reversed(specs):
        xs.sort(key=getter(key), reverse=reverse)
    return xs
