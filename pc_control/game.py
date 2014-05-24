#!/usr/bin/env python2
# -*- coding: utf8 -*-

# Code based on https://github.com/bfontaine/term2048

# TODO : best score ?

import board
import sys
import tools


class Game():
    COLORS = {
        2: {'r': 255, 'g': 255, 'b': 255},
        4: {'r': 255, 'g': 255, 'b': 255},
        8: {'r': 255, 'g': 255, 'b': 255},
        16: {'r': 255, 'g': 255, 'b': 255},
        32: {'r': 255, 'g': 255, 'b': 255},
        64: {'r': 255, 'g': 255, 'b': 255},
        128: {'r': 255, 'g': 255, 'b': 255},
        256: {'r': 255, 'g': 255, 'b': 255},
        512: {'r': 255, 'g': 255, 'b': 255}
    }
    DEFAULT_COLOR = {'r': 0, 'g': 0, 'b': 0}

    def __init__(self, ser, goal=256, size=3,
                 corrections={'r': 1.0, 'g': 1.0, 'b': 1.0},
                 brightness=1.0):
        # ser must be an opened pyserial object
        self.brd = board.Board(goal=goal, size=size)
        self.score = 0

    def end(self):
        """Returns True if the game is finished"""
        return not (self.brd.won() or self.brd.can_move())

    def update_score(self, points):
        """Updates the current score adding it the specified
        amount of points
        """
        self.score += points

    def save_score(self):
        """Saves the current score"""
        # TODO
        raise Exception("TODO")

    def loop(self):
        """Main loop"""
        # TODO
        raise Exception("TODO")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        tools.error("Usage: "+sys.argv[0]+" SERVER_IP")
    # TODO
