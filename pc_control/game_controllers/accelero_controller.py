# -*- coding: utf8 -*-
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

# This is the file and the class to use to control the game using a web
# interface with the usual 2048 game. By default, the web interface is
# accessible only from the game server at localhost:8080.

import multiprocessing
import SocketServer


class UDPHandler(SocketServer.BaseRequestHandler):
    """Handler for the UDP SocketServer"""
    def handle(self):
        """Get the data, filter it and send it to the queue"""
        data = self.request[0].strip()
        if data not in ["UP", "DOWN", "LEFT", "RIGHT"]:
            data = ""
        self.server.queue.put(data)


class ServerThread(multiprocessing.Process):
    """Thread to handle the webserver"""
    def __init__(self, queue):
        self.HOST, self.PORT = "localhost", 4243
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        """Run the SocketServer waiting for instructions"""
        try:
            server = SocketServer.UDPServer((self.HOST, self.PORT), UDPHandler)
            server.serve_forever()
        except Exception, ex:
            print ex


class AcceleroController():
    """Controller class"""
    def __init__(self):
        self.queue = multiprocessing.Queue()
        self.server_thread = ServerThread(self.queue)
        self.server_thread.start()

    def get(self):
        """Method to get the next move, blocking until a move is done"""
        return self.queue.get()

    def close(self):
        """Close method called by the Game() class to clean anything"""
        if self.server_thread.is_alive():
            self.server_thread.terminate()
            self.server_thread.join()
