# -*- coding: UTF-8 -*-

# Modified version of https://github.com/bfontaine/term2048
# Original license: MIT License, bfontaine:
#    https://github.com/bfontaine/term2048/blob/master/LICENSE

# Modifications licensed under:
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

import random


class Board(object):
    """
    A 2048 board
    """
    UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

    GOAL = 256
    SIZE = 3

    def __init__(self, goal=GOAL, size=SIZE, **kws):
        self.__size = size
        self.__size_range = xrange(0, self.__size)
        self.__goal = goal
        self.__won = False
        self.cells = [[0]*self.__size for _ in xrange(self.__size)]
        self.old_cells = [[0]*self.__size for _ in xrange(self.__size)]
        self.add_tile()
        self.add_tile()

    def size(self):
        """return the board size"""
        return self.__size

    def goal(self):
        """return the board goal"""
        return self.__goal

    def won(self):
        """
        return True if the board contains at least one tile with the board goal
        """
        return self.__won

    def can_move(self):
        """
        test if a move is possible
        """
        if not self.filled():
            return True

        for y in self.__size_range:
            for x in self.__size_range:
                c = self.get_cell(x, y)
                if (x < self.__size-1 and c == self.get_cell(x+1, y)) \
                   or (y < self.__size-1 and c == self.get_cell(x, y+1)):
                    return True

        return False

    def filled(self):
        """
        return true if the game is filled
        """
        return len(self.get_empty_cells()) == 0

    def add_tile(self, value=None, choices=([2]*9+[4])):
        """
        add a random tile in an empty cell
        value: value of the tile to add.
        choices: a list of possible choices for the value of the tile.
        default is [2, 2, 2, 2, 2, 2, 2, 2, 2, 4].
        """
        if value:
            choices = [value]

        v = random.choice(choices)
        empty = self.get_empty_cells()
        if empty:
            x, y = random.choice(empty)
            self.set_cell(x, y, v)

    def get_cell(self, x, y):
        """return the cell value at x,y"""
        return self.cells[y][x]

    def set_cell(self, x, y, v):
        """set the cell value at x,y"""
        self.cells[y][x] = v

    def get_line(self, y):
        """return the y-th line, starting at 0"""
        return self.cells[y]

    def get_col(self, x):
        """return the x-th column, starting at 0"""
        return [self.get_cell(x, i) for i in self.__size_range]

    def set_line(self, y, l):
        """set the y-th line, starting at 0"""
        self.cells[y] = l[:]

    def set_col(self, x, l):
        """set the x-th column, starting at 0"""
        for i in xrange(0, self.__size):
            self.set_cell(x, i, l[i])

    def get_empty_cells(self):
        """return a (x, y) pair for each empty cell"""
        return [(x, y)
                for x in self.__size_range
                for y in self.__size_range if self.get_cell(x, y) == 0]

    def __collapse_line_or_col(self, line, d):
        """
        Merge tiles in a line or column according to a direction and return a
        tuple with the new line and the score for the move on this line
        """
        if (d == Board.LEFT or d == Board.UP):
            inc = 1
            rg = xrange(0, self.__size-1, inc)
        else:
            inc = -1
            rg = xrange(self.__size-1, 0, inc)

        pts = 0
        for i in rg:
            if line[i] == 0:
                continue
            if line[i] == line[i+inc]:
                v = line[i]*2
                if v == self.__goal:
                    self.__won = True

                line[i] = v
                line[i+inc] = 0
                pts += v

        return (line, pts)

    def __move_line_or_col(self, line, d):
        """
        Move a line or column to a given direction (d)
        """
        nl = [c for c in line if c != 0]
        if d == Board.UP or d == Board.LEFT:
            return nl + [0] * (self.__size - len(nl))
        return [0] * (self.__size - len(nl)) + nl

    def move(self, d, add_tile=True):
        """
        move and return the move score
        """
        if d == Board.LEFT or d == Board.RIGHT:
            chg, get = self.set_line, self.get_line
        elif d == Board.UP or d == Board.DOWN:
            chg, get = self.set_col, self.get_col
        else:
            return 0

        moved = False
        score = 0

        self.old_cells = [list(i) for i in self.cells]

        for i in self.__size_range:
            # save the original line/col
            origin = get(i)
            # move it
            line = self.__move_line_or_col(origin, d)
            # merge adjacent tiles
            collapsed, pts = self.__collapse_line_or_col(line, d)
            # move it again (for when tiles are merged, because empty cells are
            # inserted in the middle of the line/col)
            new = self.__move_line_or_col(collapsed, d)
            # set it back in the board
            chg(i, new)
            # did it change?
            if origin != new:
                moved = True
            score += pts

        # don't add a new tile if nothing changed
        if moved and add_tile:
            self.add_tile()

        return score

    def get_diff(self):
        """Returns the difference between the actual board and the board as it
        was before the last move"""
        diff = []
        for x in xrange(self.__size):
            for y in xrange(self.__size):
                if self.cells[y][x] != self.old_cells[y][x]:
                    diff.append({'x': x, 'y': y, "value": self.cells[y][x]})
        return diff

    def print_brd(self):
        """Print the board nicely"""
        for x in xrange(self.__size):
            for y in xrange(self.__size):
                print(self.cells[y][x],)
                print(" | ",)
            print("\n",)
            print("---------",)
            print("\n",)
