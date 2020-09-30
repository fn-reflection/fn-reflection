import pickle
import time
import ssl
from pathlib import Path
import cloudpickle
import _io
import _thread


def to_pickle(obj, filepath: str, protocol: int):
    with open(filepath, mode='wb') as f:
        pickle.dump(obj=obj, file=f, protocol=protocol)


def to_pickle_with_timestamp(obj, protocol: int, prefix: str = '', makedirs: bool = True):
    filepath = Path(f'{prefix}{int(time.time()*1000)}')
    if makedirs:
        filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, mode='wb') as f:
        pickle.dump(obj=obj, file=f, protocol=protocol)


def from_pickle(pickle_file):
    with open(pickle_file, mode='rb') as f:
        obj = pickle.load(file=f)
    return obj


def pickle__thread_LockType(_obj):
    return lambda: _thread.LockType, ()


def pickle_ssl_SSLSocket(_obj):
    return lambda: ssl.SSLSocket, ()


def pickle__io_TextIOWrapper(_obj):
    return lambda: _io.TextIOWrapper, ()


def update_cloudpickler_dispatchtable():
    cloudpickle.CloudPickler.dispatch[_thread.LockType] = pickle__thread_LockType
    cloudpickle.CloudPickler.dispatch[ssl.SSLSocket] = pickle_ssl_SSLSocket
    cloudpickle.CloudPickler.dispatch[_io.TextIOWrapper] = pickle__io_TextIOWrapper
