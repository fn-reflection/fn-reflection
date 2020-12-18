import pickle
import time
import ssl
import threading
from pathlib import Path
import copyreg
import types
import _queue
import socketio
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


def pickle_to_none(_obj):
    return str, (str(_obj),)


def update_copyreg_dispatchtable():
    copyreg.pickle(_thread.LockType, pickle_to_none)
    copyreg.pickle(threading.Thread, pickle_to_none)
    copyreg.pickle(ssl.SSLSocket, pickle_to_none)
    copyreg.pickle(_io.TextIOWrapper, pickle_to_none)
    copyreg.pickle(types.ModuleType, pickle_to_none)
    copyreg.pickle(types.FunctionType, pickle_to_none)
    copyreg.pickle(_queue.SimpleQueue, pickle_to_none)
    copyreg.pickle(socketio.client.Client, pickle_to_none)
