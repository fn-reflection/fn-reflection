# pylint:disable=broad-except
import sys
from typing import Callable
import pickle
import traceback
from .pickle import to_pickle_with_timestamp, update_cloudpickler_dispatchtable

update_cloudpickler_dispatchtable()

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


def try_with_excepthook(procedure: Callable, excepthook: Callable, *args, **kwargs):
    try:
        res = procedure(*args, **kwargs)
        return res
    except Exception as _e:
        _, _, tb = sys.exc_info()
        excepthook(tb)


def locals_json(tb, skip_frame=0, max_frame=100):
    local_var_list = []
    for _ in range(skip_frame):
        tb = tb.tb_next
        if tb is None:
            return reversed(local_var_list)
    for _ in range(max_frame-skip_frame):
        local_var_list.append(tb.tb_frame.f_locals)
        tb = tb.tb_next
        if tb is None:
            return reversed(local_var_list)


def summary_message(tb, skip_frame=0, max_frame=10):
    stack_list = reversed(traceback.format_tb(tb)[skip_frame:max_frame])
    local_var_list = [str(local_vars) for local_vars in locals_json(tb, max_frame=max_frame)]
    return "\n".join(["\n".join(pair) for pair in zip(local_var_list, stack_list)])
