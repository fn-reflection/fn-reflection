
import time
from pathlib import Path


def to_file(obj, filepath: str):
    with open(filepath, mode='wb') as f:
        f.write(obj)


def to_file_with_timestamp(obj, prefix: str = '', makedirs: bool = True):
    filepath = Path(f'{prefix}{int(time.time()*1000)}')
    if makedirs:
        filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, mode='wb') as f:
        f.write(obj)
