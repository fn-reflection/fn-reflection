import time
import gc
from datetime import datetime
from typing import Mapping, Any, Callable,Union
from logging import Logger
from itertools import repeat
import functools
from .hash import fastdigest

def yymmdd() -> str:
    return datetime.utcnow().strftime("%y%m%d")


def yymmddhh() -> str:
    return datetime.utcnow().strftime("%y%m%d%H")


def yymmddhhmm() -> str:
    return datetime.utcnow().strftime("%y%m%d%H%M")


def yymmddhhmmss() -> str:
    return datetime.utcnow().strftime("%y%m%d%H%M%S")


def unix_time() -> str:
    return datetime.utcnow().timestamp()


def unix_time_nano() -> str:
    return int(datetime.utcnow().timestamp()*1e9)


def unix_time_jp() -> str:
    return datetime.now().timestamp()


def unix_time_nano_jp() -> str:
    return int(datetime.now().timestamp()*1e9)


def _timewatch(f, n, timer=time.perf_counter(),
               return_result=False):
    result = None
    if return_result:
        start = timer()
        for _ in repeat(None, n-1):
            f()
        result = f()
        end = timer()
        elapsed = end-start
    else:
        start = timer()
        for _ in repeat(None, n):
            f()
        end = timer()
        elapsed = end-start
    return result, elapsed


def timeit(f: Callable, setup: Callable = None, time_limit: int = 1, n: int = None,
           with_args_digest: bool = False, timer=time.perf_counter,
           out: Union[Mapping[str, Any],Logger] = None):
    gc_was_enabled = gc.isenabled()
    result = None
    try:
        if setup:
            setup()
        gc.disable()
        if n is None:
            result, test_elapsed = _timewatch(f=f, n=1, timer=timer,
                                              return_result=True)
            if test_elapsed > time_limit:
                n = 1
                elapsed = test_elapsed
            else:
                n = int(time_limit/test_elapsed) if test_elapsed != 0 else 10000
                _, elapsed = _timewatch(f=f, n=n, timer=timer,
                                        return_result=False)
        else:
            result, elapsed = _timewatch(f=f, n=n, timer=timer,
                                         return_result=True)
        args_digest =''
        if isinstance(f, functools.partial):
            name = f.func.__name__
            if with_args_digest and f.args:
                args_digest = fastdigest(f.args)
        else:
            name = f.__name__
        if out is None:
            print(f'{name}{args_digest},avg_elapsed={elapsed:2.3f}ms,n={n}')
        elif isinstance(out, dict):
            out[name+args_digest] = [elapsed/n, n]
        elif isinstance(out,Logger):
            out.debug(f'{name}{args_digest},avg_elapsed={elapsed:2.3f}ms,n={n}')
    finally:
        if gc_was_enabled:
            gc.enable()
    return result
