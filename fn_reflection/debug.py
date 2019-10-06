import time
import logging
import sys
import os
from pathlib import Path
from datetime import datetime
from fn_reflection.time import yymmdd, yymmddhh, yymmddhhmm, yymmddhhmmss
from fn_reflection.os import filedatasync

__all__ = ['setup_logger', 'success_or_warning',
           'exception_dict', 'caller_context']
NOW_RESOLUTIONS = {'1d': yymmdd, '1h': yymmddhh,
                   '1m': yymmddhhmm, '1s': yymmddhhmmss}


def setup_logger(logger: logging.Logger,
                 log_path: str,
                 fmt: str = 't:%(asctime)s\tlv:%(levelname)s\tn:%(name)s\tm:%(message)s') -> None:
    if not os.path.exists(log_path):
        print(f'log file not found, log_path:{log_path}', file=sys.stderr)
        return
    if not logger.handlers:
        fmtr = logging.Formatter(fmt)
        sh = logging.StreamHandler()
        sh.setFormatter(fmtr)
        fh = logging.FileHandler(filename=log_path)
        fh.setFormatter(fmtr)
        logger.addHandler(sh)
        logger.addHandler(fh)
    return logger


def persistent_rotate(s, file_prefix, dir_name="persistent", ext='txt', duration='1h'):
    dir_path = Path(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    file_path = dir_path / f"{file_prefix}_{NOW_RESOLUTIONS[duration]()}.{ext}"
    with file_path.open(mode='a', encoding='utf-8') as f:
        print(s, file=f)
        f.flush()
        filedatasync(f.fileno())


def success_or_warning(logger, func: callable, *args, **kwargs):
    try:
        res = func()
    except Exception as e:
        msg = e.__class__.__name__ + str(e.args)
        if logger:
            logger.warning(msg)
        else:
            print(msg, file=sys.stderr)
    else:
        return res


def exception_dict(tb, e, max_frame=5):
    d = dict(utcnow=datetime.utcnow(), exception=e, frames=[])
    for i in range(max_frame):
        frame_d = dict(where=f"file:{tb.tb_frame.f_code.co_filename},line:{tb.tb_lineno},func:{tb.tb_frame.f_code.co_name}",
                       locals={k: v for k, v in tb.tb_frame.f_locals.items() if k not in ['e', '_', 'tb', 'username', 'password']})
        d['frames'].append(frame_d)
        tb = tb.tb_next
        if tb is None:
            return d
    return d


if __name__ == "__main__":
    while True:
        time.sleep(5)
        persistent_rotate(NOW_RESOLUTIONS['1s'](), 'test')
