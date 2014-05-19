#!/usr/bin/env python2
# -*- coding: utf8 -*-

# Needs the full sketch on the LEDs
# Will blink each LED in Red, Green and Blue

# Usage : ./test_serial.py SERIAL_PORT start end
# start and end are numbers for the first and last LED to test

# If the Uno resets when launching the program, try to run
# stty -hup -F SERIAL_PORT

import serial
import time
import sys


def main(ser):
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
        main(ser)
    except:
        ser.close()
