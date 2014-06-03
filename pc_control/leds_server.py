#!/usr/bin/env python2
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


import control
import json
import SocketServer
import sys
import tools


class Server(SocketServer.TCPServer):
    """Custom SocketServer class to use extra args"""
    def __init__(self, server_address, RequestHandlerClass,
                 serial_port, nb_leds, brightness, corrections):
        SocketServer.TCPServer.__init__(self, server_address,
                                        RequestHandlerClass)
        self.serial_port = serial_port
        self.nb_leds = nb_leds
        self.brightness = brightness
        self.corrections = corrections


class ServerHandler(SocketServer.StreamRequestHandler):
    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.control = control.Control(self.server.serial_port,
                                       self.server.nb_leds,
                                       brightness=self.server.brightness,
                                       corrections=self.corrections)

    def handle(self):
        self.data = self.rfile.readline().strip()

        print "Got from {}:".format(self.client_address[0])
        print self.data

        # ACK
        self.wfile.write(len(self.data))

        # Send to the LEDs
        try:
            self.data = json.loads(self.data)
            try:
                fading_duration = self.data["fading_duration"]
            except:
                fading_duration = 0
            self.control.send_colors(self.data["colors"],
                                     fading=self.data["fading"],
                                     fading_duration=fading_duration)
        except:
            tools.error("Invalid packet")

    def finish(self):
        self.control.close()


if __name__ == '__main__':
    HOST = ''
    PORT = 4242
    nb_leds = 9
    brightness = 1.0
    corrections = {'r': 1.0, 'g': 1.0, 'b': 1.0}

    if len(sys.argv) < 2:
        print("Usage: "+sys.argv[0]+" SERIAL_PORT")
        sys.exit()

    server = Server((HOST, PORT), ServerHandler, sys.argv[1],
                    nb_leds, brightness, corrections)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nExit…")
        sys.exit()
