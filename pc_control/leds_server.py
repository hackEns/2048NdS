#!/usr/bin/env python2
# -*- coding: utf8 -*-

import control
import json
import SocketServer
import sys
import tools


class Server(SocketServer.ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass,
                 serial_port, nb_leds, brightness):
        SocketServer.ThreadingTCPServer.__init__(self, server_address,
                                                 RequestHandlerClass)
        self.serial_port = serial_port
        self.nb_leds = nb_leds
        self.brightness = brightness


class ServerHandler(SocketServer.StreamRequestHandler):
    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.control = control.Control(self.server.serial_port,
                                       self.server.nb_leds,
                                       brightness=self.server.brightness)

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

    if len(sys.argv) < 2:
        print("Usage: "+sys.argv[0]+" SERIAL_PORT")
        sys.exit()

    server = Server((HOST, PORT), ServerHandler, sys.argv[1],
                    nb_leds, brightness)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nExit…")
        sys.exit()
