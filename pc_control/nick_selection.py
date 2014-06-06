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

# Code used to handle nick selection

import multiprocessing
import os
from bottle import Bottle, static_file, request


class NickThread(multiprocessing.Process):
    """Thread to handle the webserver"""
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.app = Bottle()
        self.queue = queue
        self.path = os.path.dirname(os.path.realpath(__file__))

    def run(self):
        """Serve the webapp with bottle, and handle moves sent via JS"""
        @self.app.route('/<filename:path>')
        def send_static(filename):
            return static_file(filename,
                               root=(self.path + "/../frontend_nick"))

        @self.app.route('/')
        def send_static_index():
            return static_file('index.html',
                               root=(self.path + "/../frontend_nick"))

        @self.app.route('/communicate')
        def get():
            self.queue.put(request.query.nick or "")
            return 'ACK'

        try:
            self.app.run(quiet=True)
        except Exception, ex:
            print ex


class Nick():
    """Controller class"""
    def __init__(self):
        self.queue = multiprocessing.Queue()
        self.nick_thread = NickThread(self.queue)
        self.nick_thread.start()

    def get(self):
        """Method to get the nick, blocking until a move is done"""
        os.system("clear")
        print("Launch your browser at http://localhost:8080 to enter nick")
        return self.queue.get()

    def close(self):
        """Close method called to clean anything"""
        if self.nick_thread.is_alive():
            self.nick_thread.terminate()
            self.nick_thread.join()


def get_nick():
    nick_class = Nick()
    nick = nick_class.get()
    nick_class.close()
    return nick
