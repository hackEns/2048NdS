#!/usr/bin/env python2
# -*- coding: utf8 -*-

from __future__ import print_function
import game
import serial
import sys


def error(*objs):
    """Write warnings to stderr"""
    printed = [i.encode('utf-8') for i in objs]
    print("ERROR: ", *printed, file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage: "+sys.argv[0]+" SERIAL_PORT")
    ser = serial.Serial(port=sys.argv[1], baudrate=115200)
    try:
        ser.open()
    except Exception, e:
        error("Error opening serial port: " + str(e))
        sys.exit(1)
    if not ser.isOpen():
        error("Serial port not opened")
        sys.exit(1)
    ser.flushInput()
    ser.flushOutput()
    try:
        game.Game(ser, goal=256, size=3,
                  corrections={'r': 1.0, 'g': 1.0, 'b': 1.0},
                  brightness=1.0).loop()
    except KeyboardInterrupt:
        sys.exit()
    finally:
        if ser.isOpen():
            ser.close()
