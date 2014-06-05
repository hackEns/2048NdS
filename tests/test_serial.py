#!/usr/bin/env python2
# -*- coding: utf8 -*-

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
#                                                       Phyks for hackEns
# -----------------------------------------------------------------------------


import serial
import time
import sys


def main(ser, start, end):
    for k in range(start, end):
        for j in [0x80+k, 127, 0, 0]:
            ser.write(chr(j))
            time.sleep(0.004)
        time.sleep(0.5)
        for j in [0x80+k, 0, 127, 0]:
            ser.write(chr(j))
            time.sleep(0.004)
        time.sleep(0.5)
        for j in [0x80+k, 0, 0, 127]:
            ser.write(chr(j))
            time.sleep(0.004)
        time.sleep(0.5)
    ser.close()


if __name__ == '__main__':
    if(len(sys.argv) < 4):
        sys.exit("Usage : "+sys.argv[0]+" SERIAL_PORT start end")

    try:
        ser = serial.Serial(sys.argv[1], 115200)
    except:
        sys.exit("Unable to open serial port.")

    try:
        main(ser, int(sys.argv[2]), int(sys.argv[3]))
    except:
        ser.close()
