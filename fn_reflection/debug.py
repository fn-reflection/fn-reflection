__all__ = ['setup_logger', 'success_or_warning',
           'exception_dict', 'caller_context']
import logging
import sys
import os


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
