# pylint:disable=broad-except
import sys
from typing import Callable
import pickle
import traceback
from tblib import pickling_support
from .pickle import to_pickle_with_timestamp
pickling_support.install()


def try_with_dump_traceback(procedure: Callable, logger, file_prefix: str = '',
                            pickle_protocol: int = pickle.HIGHEST_PROTOCOL, makedirs=True):
    try:
        procedure()
    except Exception as e:
        _, _, tb = sys.exc_info()
        print(traceback.format_exc())
        logger.error(e)
        to_pickle_with_timestamp(
            obj=tb, prefix=file_prefix, makedirs=makedirs, protocol=pickle_protocol)


def try_with_post_mortem(procedure: Callable, callback: Callable, *args, **kwargs):
    try:
        res = procedure(*args, **kwargs)
        return res
    except Exception as _e:
        _, _, tb = sys.exc_info()
        callback(tb)


def locals_json(tb, max_frame=100):
    local_var_list = []
    for _ in range(max_frame):
        local_vars = dict(tb.tb_frame.f_locals.items())
        local_var_list.append(local_vars)
        tb = tb.tb_next
        if tb is None:
            break
    return local_var_list


def summary_message(tb, max_frame=10):
    stack_list = traceback.format_tb(tb)[:max_frame]
    local_var_list = [str(local_vars) for local_vars in locals_json(tb, max_frame=max_frame)]
    return "\n".join(["\n".join(pair) for pair in zip(local_var_list, stack_list)])
