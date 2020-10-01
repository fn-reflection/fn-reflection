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


def try_with_excepthook(procedure: Callable, excepthook: Callable, *args, **kwargs):
    try:
        res = procedure(*args, **kwargs)
        return res
    except Exception as _e:
        _, _, tb = sys.exc_info()
        excepthook(tb)


def locals_json(tb, depth, frames):
    local_var_list = []
    skips = max(depth-frames, 0)
    for _ in range(skips):
        tb = tb.tb_next
    for _ in range(depth-skips):
        tb = tb.tb_next
        local_var_list.append(tb.tb_frame.f_locals)
    return reversed(local_var_list)


def summary_message(tb, depth, frames):
    local_var_list = [str(local_vars) for local_vars in locals_json(tb, depth=depth, frames=frames)]
    stack_list = reversed(traceback.format_tb(tb)[-frames:])
    return "\n".join(["\n".join(pair) for pair in zip(local_var_list, stack_list)])


def traceback_depth(tb) -> int:
    res = 0
    while tb.tb_next is not None:
        res += 1
        tb = tb.tb_next
    return res


def excepthook_for_discord(discord_connector, tb, summary_frames, tb_frames):
    depth = traceback_depth(tb)
    summary = summary_message(tb, depth=depth, frames=summary_frames)
    locals_pickle = pickle.dumps(obj=locals_json(tb, depth=depth, frames=tb_frames))
    locals_filename = f"locals_{yymmddhhmmss()}_{hashlib.md5(locals_pickle).hexdigest()}.pickle"
    loading_script = f"fn_reflection.pickle.from_pickle('{locals_filename}')"
    message = {'content': f"{loading_script}\n{summary}"[:2000],
               'file': {locals_filename: locals_pickle, 'summary.yml': summary}}
    discord_post(discord_connector, message)


def discord_post(discord_connector, message):
    if isinstance(message, str):
        discord_connector.post(content=message)
    elif isinstance(message, dict):
        discord_connector.post(**message)
