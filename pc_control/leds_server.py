#!/usr/bin/env python2
# -*- coding: utf8 -*-

import control
import json
import SocketServer
import sys


class Server(SocketServer.ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass,
                 arg1, arg2, arg3):
        SocketServer.ThreadingTCPServer.__init__(self, server_address,
                                                 RequestHandlerClass)
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3


class ServerHandler(SocketServer.BaseRequestHandler):
    def __init__(self, server_address, RequestHandlerClass,
                 serial_port, nb_leds, brightness):
        self.serial_port = serial_port
        self.nb_leds = nb_leds
        self.brightness = brightness

    def setup(self):
        self.control = control.Control(self.serial_port, self.nb_leds,
                                       brightness=self.brightness)

    def handle(self):
        self.data = self.rfile.readline().strip()

        print "Got from {}:".format(self.client_address[0])
        print self.data

        # ACK
        self.wfile.write(len(self.data))

        # Send to the LEDs
        self.data = json.loads(self.data)
        try:
            fading_duration = self.data['fading_duration']
        except:
            fading_duration = 0
        self.control.send_colors(self.data.colors,
                                 fading=self.data.fading,
                                 fading_duration=fading_duration)

    def finish(self):
        self.control.close()


if __name__ == '__main__':
    HOST = ''
    PORT = 4242
    nb_leds = 9
    brightness = 1.0

    if len(sys.argv) < 2:
        print("Usage: "+sys.argv[0]+" SERIAL_PORT")
        sys.exit()

    server = Server((HOST, PORT), ServerHandler, sys.argv[1],
                    nb_leds, brightness)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nExit…")
