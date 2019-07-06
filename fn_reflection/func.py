__all__ = ['setup_logger', 'partitionby',
           'caller_context', 'unregistered_data']
import fn_reflection._external as _e


def multiple_sort(xs, specs):
    if isinstance(specs, list) or isinstance(specs, tuple):
        getter = _e.operator.itemgetter
    else:
        getter = _e.operator.attrgetter
    for key, reverse in reversed(specs):
        xs.sort(key=getter(key), reverse=reverse)
    return xs


def setup_logger(logger: _e.logging.Logger,
                 log_path: str,
                 fmt: str = 't:%(asctime)s\tlv:%(levelname)s\tn:%(name)s\tm:%(message)s') -> None:
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


def success_or_warning(logger, func: callable, *args, **kwargs):
    try:
        res = func()
    except Exception as e:
        msg = e.__class__.__name__ + str(e.args)
        if logger:
            logger.warning(msg)
        else:
            print(msg, file=_e.sys.stderr)
    else:
        return res


def partitionby(coll, f):
    flip_flop = False

    def switch(item):
        nonlocal flip_flop
        if f(item):
            flip_flop = not flip_flop
        return flip_flop
    return map(lambda grp: list(grp[1]),
               _e.itertools.groupby(coll, switch))


def caller_context():
    x = _e.inspect.stack()[1]
    return f'file:{x[1]}\tline:{x[2]}\tfuncname:{x[3]}'
