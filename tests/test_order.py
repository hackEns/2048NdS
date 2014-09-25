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
# elarnon (basile@clement.pm) wrote or updated these files for hackEns. As long
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
import curses

class Board:
    def __init__(self, ser, nrows, ncols):
        self.ser = ser
        self.nrows = nrows
        self.ncols = ncols
        self.start = 0
        self.end = nrows * ncols
        self.stdscr = None

    def __enter__(self):
        if self.stdscr is not None:
            raise Exception("Already in curses.")
        # See https://docs.python.org/2/howto/curses.html
        self.stdscr = curses.initscr()
        # Colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_RED)
        # Disable automatic display
        curses.noecho()
        # Don't wait for line break
        curses.cbreak()
        # Handle special keys e.g. KEY_DOWN/UP/LEFT/RIGHT
        self.stdscr.keypad(1)

    def __exit__(self, type, value, traceback):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        self.stdscr = None

    def color(self, ids, r, g, b):
        for k in ids:
            for j in [0x80+k, int(r / 2), int(g / 2), int(b / 2)]:
                ser.write(chr(j))

    def draw_grid(self):
        stdscr = self.stdscr
        for i in range(self.nrows - 1):
            stdscr.hline(2 * i + 1, 0, curses.ACS_HLINE, 4 * self.ncols - 1)
        for i in range(self.ncols - 1):
            stdscr.vline(0, 4 * i + 3, curses.ACS_VLINE, 2 * self.nrows - 1)
        for i in range(self.nrows - 1):
            for j in range(self.ncols - 1):
                stdscr.addch(2 * i + 1, 4 * j + 3, curses.ACS_PLUS)

    def calibrate(self):
        stdscr = self.stdscr
        stdscr.clear()
        self.draw_grid()
        stdscr.refresh()
        self.color(range(self.start, self.end), 0, 0, 0)
        stdscr.move(0, 0)
        order = []
        for cur in range(self.start, self.end):
            self.color([cur], 255, 255, 255)
            while True:
                c = stdscr.getch()
                (y, x) = stdscr.getyx()
                if c == curses.KEY_RIGHT:
                    stdscr.move(y, min(self.ncols * 4 - 4, x + 4))
                elif c == curses.KEY_LEFT:
                    stdscr.move(y, max(0, x - 4))
                elif c == curses.KEY_UP:
                    stdscr.move(max(0, y - 2), x)
                elif c == curses.KEY_DOWN:
                    stdscr.move(min(self.nrows * 2 - 2, y + 2), x)
                elif c == ord('x') and (y / 2, x / 4) not in order:
                    stdscr.addstr('{:03}'.format(cur), curses.color_pair(1))
                    stdscr.move(y, x)
                    stdscr.refresh()
                    order.append((y / 2, x / 4))
                    break
            self.color([cur], 0, 0, 0)
        result = [ [ 0 for i in range(self.ncols) ] for j in range(self.nrows)]
        cur = 0
        for (y, x) in order:
            result[y][x] = cur
            cur += 1
        return result

if __name__ == '__main__':
    if(len(sys.argv) < 4):
        sys.exit("Usage : "+sys.argv[0]+" SERIAL_PORT nrows ncols ")

    try:
        ser = serial.Serial(sys.argv[1], 115200)
        nrows = int(sys.argv[2])
        ncols = int(sys.argv[3])
        board = Board(ser, nrows, ncols)
    except:
        sys.exit("Unable to open serial port.")

    try:
        with board:
            order = board.calibrate()
        print(order)
    except:
        ser.close()
