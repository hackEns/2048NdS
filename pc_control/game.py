#!/usr/bin/env python2
# -*- coding: utf8 -*-

# Code based on https://github.com/bfontaine/term2048

import board
import game_controllers.keyboard_controller as kb_ctrl
# TODO : web controller + smartphone controller
import json
import socket
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
    SCORES_FILE = "TODO"  # TODO

    def __init__(self, server_address, game_controller, nick,
                 goal=256, size=3):
        self.brd = board.Board(goal=goal, size=size)
        self.score = 0
        self.server_address = server_address
        self.game_controller = game_controller()
        self.nick = nick

    def end(self):
        """Returns True if the game is finished"""
        return (self.brd.won() or not self.brd.can_move())

    def update_score(self, points):
        """Updates the current score adding it the specified
        amount of points
        """
        self.score += points

    def save_score(self):
        """Saves the current score"""
        # TODO
        raise Exception("TODO")

    def send_instructions(self):
        """Sends instructions to the LEDs server to display the current
        configuration
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect(self.server_address)
            data = "TODO"
            sock.sendall(json.dumps(data) + "\n")
            received = sock.recv(1024)
            # TODO check len received
            # TODO
        finally:
            sock.close()

    def readMove(self):
        """Reads the move from the controller and
        maps it to Board.{UP,DOWN,LEFT,RIGHT}
        """
        m = self.game_controller.get()
        if m == "LEFT":
            return board.Board.LEFT
        elif m == "RIGHT":
            return board.Board.RIGHT
        elif m == "UP":
            return board.Board.UP
        elif m == "DOWN":
            return board.Board.DOWN
        else:
            return 0

    def loop(self):
        """Main loop"""
        while True:
            if not self.end():
                break
            m = self.readMove()
            self.send_instructions()
            self.update_score(self.brd.move(m))
        self.save_score()
        # TODO : Special kitsch blink
        if self.brd.won():
            print('You won')
        else:
            print('Game over')
        return self.score


if __name__ == "__main__":
    if len(sys.argv) < 2:
        tools.error("Usage: "+sys.argv[0]+" SERVER_IP")
    HOST = sys.argv[1]
    PORT = 4242

    try:
        while True:
            nick = raw_input("Nick ? ")
            Game((HOST, PORT), kb_ctrl.KeyboardController, nick).loop()
    except KeyboardInterrupt:
        print("\nExit…")
        sys.exit()
