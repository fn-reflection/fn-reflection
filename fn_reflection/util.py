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
    def list_or_tuple(x):
        return isinstance(x, list) or isinstance(x, tuple)
    for farg in fargs:
        if not list_or_tuple(farg):
            f = farg
            val = f(value)
        else:
            f, arg = farg
            if isinstance(arg, dict):
                val = f(value, **arg)
            elif list_or_tuple(arg):
                val = f(value, *arg)
            else:
                val = f(value, arg)
    return val
