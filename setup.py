#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup

if not sys.version_info[:2] >= (3, 5):
    raise RuntimeError("Python version >= 3.5 required.")


def main():
    setup()


if __name__ == '__main__':
    main()
