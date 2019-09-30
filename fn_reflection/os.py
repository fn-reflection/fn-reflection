import os
import platform

def filedatasync(fd):
    if os.name=='posix':
        os.fdatasync(fd)
        return
    if platform.system()=='Windows':
        os.fsync(fd)
        return