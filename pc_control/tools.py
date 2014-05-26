# -*- coding: utf8 -*-
# -----------------------------------------------------------------------------
# "THE NO-ALCOHOL BEER-WARE LICENSE" (Revision 42):
# Phyks (webmaster@phyks.me) wrote or updated these files for hackEns. As long
# as you retain this notice you can do whatever you want with this stuff 
# (and you can also do whatever you want with this stuff without retaining it, 
# but that's not cool...).
#
# If we meet some day, and you think this stuff is worth it, you can buy us a 
# <del>beer</del> soda in return.
#                                                       Phyks for hackEns
# -----------------------------------------------------------------------------

from __future__ import print_function
import sys


def error(*objs):
    """Write warnings to stderr"""
    printed = [i.encode('utf-8') for i in objs]
    print("ERROR: ", *printed, file=sys.stderr)
