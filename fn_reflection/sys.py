import inspect
import typing


def caller_context():
    x = inspect.stack()[1]
    return f'file:{x[1]}\tline:{x[2]}\tfuncname:{x[3]}'


def run_in_daemon_thread(func):
    t = threading.Thread(target=func, daemon=True)
    t.start()
    return t


def run_once(f: typing.Callable):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper
