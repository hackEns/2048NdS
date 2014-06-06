#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Needs the full sketch on the LEDs
# Will blink each LED in Red, Green and Blue

# Usage : ./test_serial.py SERIAL_PORT start end
# start and end are numbers for the first and last LED to test

# If the Uno resets when launching the program, try to run
# stty -hup -F SERIAL_PORT

# -----------------------------------------------------------------------------
# "THE NO-ALCOHOL BEER-WARE LICENSE" (Revision 42):
# Phyks (webmaster@phyks.me) wrote or updated these files for hackEns. As long
# as you retain this notice you can do whatever you want with this stuff
# (and you can also do whatever you want with this stuff without retaining it,
# but that's not cool...).
#
# If we meet some day, and you think this stuff is worth it, you can buy us a
# <del>beer</del> soda in return.
#                                                       elarnon for hackEns
# -----------------------------------------------------------------------------

import serial
import sys
import os
from keypress import getKey, UP, DOWN, RIGHT, LEFT


def send_color(start, end, r, g, b):
    for k in range(start, end):
        for j in [0x80+k, int(r / 2), int(g / 2), int(b / 2)]:
            ser.write(chr(j))


def main(ser, start, end):
    c = [255, 255, 255]
    cur = 0
    while True:
        os.system('clear')
        if cur == 0:
            print("\x1b[41m{:03}\x1b[m {:03} {:03}".format(c[0], c[1], c[2]))
        elif cur == 1:
            print("{:03} \x1b[42m{:03}\x1b[m {:03}".format(c[0], c[1], c[2]))
        elif cur == 2:
            print("{:03} {:03} \x1b[44m{:03}\x1b[m".format(c[0], c[1], c[2]))
        send_color(start, end, c[0], c[1], c[2])
        k = getKey()
        if k == UP:
            if c[cur] < 255:
                c[cur] += 1
        elif k == DOWN:
            if c[cur] > 0:
                c[cur] -= 1
        elif k == RIGHT:
            cur = (cur + 1) % 3
        elif k == LEFT:
            cur = (cur - 1) % 3


if __name__ == '__main__':
    if(len(sys.argv) < 4):
        sys.exit("Usage : "+sys.argv[0]+" SERIAL_PORT start end")

    try:
        ser = serial.Serial(sys.argv[1], 115200)
        start = int(sys.argv[2])
        end = int(sys.argv[3])
    except:
        sys.exit("Unable to open serial port.")

    try:
        main(ser, start, end)
    except:
        ser.close()
