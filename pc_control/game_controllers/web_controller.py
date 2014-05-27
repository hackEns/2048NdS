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
from bottle import Bottle, static_file, request


class WebServerThread(multiprocessing.Process):
    """Thread to handle the webserver"""
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.app = Bottle()
        self.queue = queue

    def run(self):
        """Serve the webapp with bottle, and handle moves sent via JS"""
        @self.app.route('/<filename:path>')
        def send_static(filename):
            return static_file(filename, root='../frontend')

        @self.app.route('/')
        def send_static_index():
            return static_file('index.html', root='../frontend')

        @self.app.route('/communicate')
        def get():
            self.queue.put(request.query.move or "")
            return 'ACK'

        try:
            self.app.run(quiet=True)
        except Exception, ex:
            print ex


class WebController():
    """Controller class"""
    def __init__(self):
        self.queue = multiprocessing.Queue()
        self.webserver_thread = WebServerThread(self.queue)
        self.webserver_thread.start()

    def get(self):
        """Method to get the next move, blocking until a move is done"""
        return self.queue.get()

    def close(self):
        """Close method called by the Game() class to clean anything"""
        if self.webserver_thread.is_alive():
            self.webserver_thread.terminate()
            self.webserver_thread.join()
