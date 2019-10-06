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
