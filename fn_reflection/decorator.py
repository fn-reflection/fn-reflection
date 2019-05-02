__all__ = ['run_once']
import fn_reflection._external as _e


def run_once(f: _e.typing.Callable):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper
