# pylint: disable=missing-docstring,invalid-name
# %%
__all__ = ['run_once', 'chain']
import fn_reflection._capcell as _capcell


def run_once(f: _capcell.typing.Callable):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def chain(value, fargs: _capcell.typing.Iterable):
    for farg in fargs:
        if not isinstance(farg, _capcell.collections.abc.Iterable):
            f = farg
            val = f(value)
        else:
            f, arg = farg
            if isinstance(arg, dict):
                val = f(value, **arg)
            elif isinstance(arg, _capcell.collections.abc.Iterable):
                val = f(value, *arg)
            else:
                val = f(value, arg)
    return val
