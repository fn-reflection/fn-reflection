# pylint:disable=dangerous-default-value
import time
import inspect
import typing
import threading


def caller_context():
    x = inspect.stack()[1]
    return f'file:{x[1]}\tline:{x[2]}\tfuncname:{x[3]}'


def run_in_daemon_thread(func, args=(), kwargs={}):
    t = threading.Thread(target=func, daemon=True, args=args, kwargs=kwargs)
    t.start()
    return t


def wait_sigint(wait_interval=10000):
    try:
        while True:
            time.sleep(wait_interval)
    except KeyboardInterrupt:
        pass


def run_once(f: typing.Callable):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def get_runtime():
    get_ipython = inspect.stack()[1].frame.f_globals.get('get_ipython')
    if not get_ipython:
        return 'python'
    if get_ipython().__class__.__name__ == 'TerminalInteractiveShell':
        return 'ipython'
    return 'jupyter'
