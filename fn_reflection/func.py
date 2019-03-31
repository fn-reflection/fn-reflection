# pylint: disable=missing-docstring,invalid-name
# %%
__all__ = ['setup_logger', 'partitionby']
import fn_reflection._external as _e


def setup_logger(logger: _e.logging.Logger,
                 log_path: str,
                 fmt: str = 't:%(asctime)s\tlv:%(levelname)s\tn:%(name)s\tm:%(message)s')->None:
    if not _e.os.path.exists(log_path):
        print(f'log file not found, log_path:{log_path}', file=_e.sys.stderr)
        return
    if not logger.handlers:
        fmtr = _e.logging.Formatter(fmt)
        sh = _e.logging.StreamHandler()
        sh.setFormatter(fmtr)
        fh = _e.logging.FileHandler(filename=log_path)
        fh.setFormatter(fmtr)
        logger.addHandler(sh)
        logger.addHandler(fh)
    return logger


def partitionby(coll, f):
    flip_flop = False

    def switch(item):
        nonlocal flip_flop
        if f(item):
            flip_flop = not flip_flop
        return flip_flop
    return map(lambda grp: list(grp[1]),
               _e.itertools.groupby(coll, switch))
