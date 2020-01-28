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
