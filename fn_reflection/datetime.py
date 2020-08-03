from datetime import datetime, timedelta


def utcpast(**args):
    return datetime.utcnow() - timedelta(**args)
