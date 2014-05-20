#!/usr/bin/env python2
# -*- coding: utf8 -*-

# All colors are in [0,255] but we have to send values between [0,127]


class Control():
    def __init__(self, ser, nb_leds,
                 corrections={'r': 1.0, 'g': 1.0, 'b': 1.0},
                 brightness=1.0):
        self.corrections = {k: brightness * corrections[k]
                            for k in corrections}
        self.ser = ser
        self.nb_leds = nb_leds
        self.current_colors = [{'r': 255, 'g': 0, 'b': 0}
                               for i in range(nb_leds)]

    def get_current_colors(self, id=None):
        if id is None:
            return self.current_colors
        else:
            return self.current_colors[id]

    def correct_color(self, color):
        """Corrects the color to match real LED render

        params: color a {r, g, b} dict
        returns: a color dict
        """
        return {i: color[i] * self.corrections[i] >> 1 for i in color}

    def send_color(self, id, color):
        """Corrects the color and send it over serial"""
        data = [0x80 + id]
        data.extend(v for k, v in self.correct_color(color).iteritems())
        for i in data:
            self.ser.write(chr(i))
        self.current_color[id] = color

    def send_colors(self, colors):
        """Send the colors to all the LEDs"""
        for i in range(min(self.nb_leds,len(colors)-1)):
            self.send_color(i, colors[i])

    def reset(self):
        """Resets all the LEDs to red"""
        for k in range(self.nb_leds):
            for i in [0x80 + k, 127, 0, 0]:
                self.ser.write(chr(i))
