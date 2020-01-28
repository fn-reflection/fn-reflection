import pickle
import time
from pathlib import Path


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
