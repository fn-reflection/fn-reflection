import time
from datetime import datetime
 
def yymmdd():
    d = datetime.utcnow().strftime("%y%m%d")


def yymmddhh():
    return datetime.utcnow().strftime("%y%m%d%H")


def yymmddhhmm():
    return datetime.utcnow().strftime("%y%m%d%H%M")


def yymmddhhmmss():
    return datetime.utcnow().strftime("%y%m%d%H%M%S")


def unix_time():
    return datetime.utcnow().timestamp()


def unix_time_nano():
    return int(datetime.utcnow().timestamp()*1e9)


def unix_time_jp():
    return datetime.now().timestamp()


def unix_time_nano_jp():
    return int(datetime.now().timestamp()*1e9)


def timeit(func):
    def decorate(*args, **kw):
        n = kw.get('timeit_iter',1)
        t_start = time.time()
        for _ in range(n):
            result = func(*args, **kw)
        t_end = time.time()
        elapsed = t_end-t_start
        if 'timeit_logger' in kw:
            kw['timeit_logger'][f"{func.__name__}_{n}"] = elapsed
        else:
            print(f'{func.__name__}, {elapsed:2.5f} ms')
        return result
    return decorate