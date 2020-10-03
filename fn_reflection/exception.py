# pylint:disable=broad-except
import sys
from typing import Callable
import hashlib
import pickle
import traceback
from .pickle import to_pickle_with_timestamp
from .time import yymmddhhmmss
from .pickle import update_copyreg_dispatchtable
update_copyreg_dispatchtable()


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


def try_with_excepthook(procedure: Callable, excepthook: Callable):
    try:
        res = procedure()
        return res
    except Exception as _e:
        e_type, e_val, tb = sys.exc_info()
        excepthook(e_type, e_val, tb)


def locals_json(tb, depth, frames):
    local_var_list = []
    skips = max(depth-frames, 0)
    for _ in range(skips):
        tb = tb.tb_next
    for _ in range(depth-skips):
        tb = tb.tb_next
        local_var_list.append(tb.tb_frame.f_locals)
    return reversed(local_var_list)


def pretty_local_vars(local_vars):
    return "\n".join([f"{k}:{v}" for k, v in local_vars.items()])


def summary_message(e_type, e_val, tb, depth, frames):
    local_var_list = [pretty_local_vars(local_vars) for local_vars in locals_json(tb, depth=depth, frames=frames)]
    stack_list = reversed(traceback.format_tb(tb)[-frames:])
    stack_summary = "\n".join(["\n".join(pair) for pair in zip(local_var_list, stack_list)])
    return f"{e_type},{e_val}\n{stack_summary}"


def traceback_depth(tb) -> int:
    res = 0
    while tb.tb_next is not None:
        res += 1
        tb = tb.tb_next
    return res


def excepthook_for_discord(discord_connector, e_type, e_val, tb, summary_frames):
    depth = traceback_depth(tb)
    summary = summary_message(e_type, e_val, tb, depth=depth, frames=summary_frames)
#    locals_pickle = pickle.dumps(obj=locals_json(tb, depth=depth, frames=tb_frames))
    locals_filename = f"locals_{yymmddhhmmss()}.txt"
    message = {'content': f"{summary}"[:2000],
               'file': {locals_filename: summary}}
    discord_post(discord_connector, message)


def discord_post(discord_connector, message):
    if isinstance(message, str):
        discord_connector.post(content=message)
    elif isinstance(message, dict):
        discord_connector.post(**message)
