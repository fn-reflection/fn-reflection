__all__ = ['setup_logger', 'partitionby',
           'caller_context', 'unregistered_data']
import fn_reflection._external as _e


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


def unregistered_data(df1: _e.pandas.DataFrame, df2: _e.pandas.DataFrame, identify):
    if (not df2) or df2.empty:
        return df1
    midf1 = df1.set_index(identify)
    midf2 = df2.drop_duplicates(identify).set_index(identify)
    joined = _e.pandas.concat([midf1, midf2], axis=1, keys=['a', 'b'])
    remove_dup = joined[joined.loc[:, ('b', '_id')].isna()]
    if 'a' in remove_dup.columns:
        return remove_dup['a'].reset_index()
    return remove_dup.reset_index()
