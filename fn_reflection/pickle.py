import pickle
import time
import os
from pathlib import Path


def to_pickle4(obj, filename):
    with open(filename, mode='wb') as f:
        pickle.dump(obj=obj, file=f, protocol=4)


def to_pickle4_with_timestamp(obj, prefix='', makedirs=True):
    filepath = Path(f'{prefix}{int(time.time()*1000)}')
    if makedirs:
        filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, mode='wb') as f:
        pickle.dump(obj=obj, file=f, protocol=4)
