# -*- coding: utf8 -*-

# File from https://github.com/bfontaine/term2048
# Original license: MIT License, bfontaine:
#    https://github.com/bfontaine/term2048/blob/master/LICENSE

# This is the file and class to use to control the game with a classical
# keyboard on the game server computer.

import multiprocessing
import pygame


class JoystickControllerThread(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.joystick.get_button(0):
                        self.queue.put("LEFT")
                    elif self.joystick.get_button(1):
                        self.queue.put("DOWN")
                    elif self.joystick.get_button(2):
                        self.queue.put("UP")
                    elif self.joystick.get_button(3):
                        self.queue.put("RIGHT")


class Controller():
    """Controller class"""
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.queue = multiprocessing.Queue()
        self.joystick_thread = JoystickControllerThread(self.queue)
        self.joystick_thread.start()

    def get(self):
        """Method to get the next move (blocking until a move is returned)"""
        return self.queue.get()

    def close(self):
        """Close method called by the Game() class to clean anything"""
        if self.joystick_thread.is_alive():
            self.joystick_thread.terminate()
            self.joystick_thread.join()
