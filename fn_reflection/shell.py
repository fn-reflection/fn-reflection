import subprocess
import sys
from traceback import format_exc
from dataclasses import dataclass


def run_script(shell_script: str) -> bytes:
    try:
        return subprocess.run(shell_script, shell=True, check=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT).stdout
    except subprocess.CalledProcessError:
        print(format_exc(), file=sys.stderr)
        return b''


def processes_by_regex(regex: str, header: bool = False):
    sh_body = f'ps -ef | grep "{regex}"| grep -v grep'
    lines = [l.split() for l
             in run_script(sh_body).decode('UTF-8').strip('\n').split('\n')]
    lines = [[*t[:7], " ".join(t[7:])] for t in lines]
    if not header:
        return lines
    sh_header = 'ps -ef|head -n 1'
    header = run_script(sh_header).decode('UTF-8').strip('\n').split()
    return [dict(zip(header, l))for l in lines]
