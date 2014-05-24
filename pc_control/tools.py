# -*- coding: utf8 -*-
from __future__ import print_function
import sys


def error(*objs):
    """Write warnings to stderr"""
    printed = [i.encode('utf-8') for i in objs]
    print("ERROR: ", *printed, file=sys.stderr)
