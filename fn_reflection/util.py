# pylint: disable=missing-docstring,invalid-name
# %%
import typing
import collections


def run_once(f: typing.Callable):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def chain(value, fargs: typing.Iterable):
    for farg in fargs:
        if not isinstance(farg, collections.abc.Iterable):
            f = farg
            val = f(value)
        else:
            f, arg = farg
            if isinstance(arg, dict):
                val = f(value, **arg)
            elif isinstance(arg, collections.abc.Iterable):
                val = f(value, *arg)
            else:
                val = f(value, arg)
    return val
