#!/usr/bin/env python2
# -*- coding: utf8 -*-

# Code based on https://github.com/bfontaine/term2048
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


import board
import game_controllers.keyboard_controller as kb_ctrl
# TODO : smartphone controller
import json
import requests
import socket
import sys
import tools


class Game():
    """The class that handles the game itself and send instructions to the LEDs
    accordingly
    """
    COLORS = {
        0: {'r': 0, 'g': 0, 'b': 0},
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
    SCORES_FILE = "scores.dat"
    REMOTE_SCORES_URL = "http://hackens.org/NdS/"
    REMOTE_SCORES_PARAMS = {'api_key': "API_KEY"}

    def __init__(self, server_address, game_controller, nick,
                 goal=256, size=3):
        self.brd = board.Board(goal=goal, size=size)
        self.score = 0
        self.server_address = server_address
        self.game_controller = game_controller()
        self.nick = nick
        self.size = size

    def __enter__(self):
        return self

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
        with open(self.SCORES_FILE, 'a') as fh:
            fh.write(self.nick+"\t"+str(self.score))
        # Send to remote server
        params = self.REMOTE_SCORES_PARAMS
        params["nick"] = self.nick
        params["score"] = self.score
        try:
            r = requests.get(self.REMOTE_SCORES_URL, params=params)
            if r.status_code != 200 or 'ack' not in r.text:
                tools.error("Unable to post high score.")
        except requests.exceptions.ConnectionError as e:
            tools.error("Network error when submitting high score:"+str(e))

    def won_animation(self):
        """Handle the animation when the player wins"""
        # TODO
        raise Exception("TODO")

    def game_over_animation(self):
        """Handle the animation when the player looses"""
        # TODO
        raise Exception("TODO")

    def get_diff(self):
        """Returns the difference between previous and current state"""
        data = {"fading": False, "colors": {}}
        data["colors"] = {self.size*k['x']+k['y']: self.COLORS[k["value"]]
                          for k in self.brd.get_diff()}
        return data

    def initialize_leds(self):
        """Returns a dict with the default color to send to the LEDs with
        send_instructions()
        """
        return {"fading": False, "colors": {k: self.COLORS[0] for k in
                                            xrange(self.size**2)}}

    def send_instructions(self, data):
        """Sends instructions to the LEDs server to display the current
        configuration

        params:
            data is a dict {fading: bool, colors: {}}, cf get_diff
        """
        if len(data["colors"]) == 0:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect(self.server_address)
            data = json.dumps(data) + "\n"
            sock.sendall(data)
            received = sock.recv(1024)
            if int(received) != len(data.strip()):
                tools.error("Error while sending instructions for LEDs")
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
        self.send_instructions(self.initialize_leds())
        while True:
            if self.end():
                break
            self.send_instructions(self.get_diff())
            m = self.readMove()
            self.update_score(self.brd.move(m))
        self.save_score()
        if self.brd.won():
            print('You won')
            self.won_animation()
        else:
            print('Game over')
            self.game_over_animation()
        return self.score

    def close(self):
        """Handle the cleaning, if necessary"""
        if hasattr(self.game_controller, 'close'):
            self.game_controller.close()

    def __exit__(self, type, value, traceback):
        self.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        tools.error("Usage: "+sys.argv[0]+" SERVER_IP")
        sys.exit(1)
    HOST = sys.argv[1]
    PORT = 4242

    try:
        while True:
            nick = raw_input("Nick ? ")
            with Game((HOST, PORT), kb_ctrl.KeyboardController, nick) as game:
                game.loop()
    except KeyboardInterrupt:
        print("\nExit…")
        sys.exit()
