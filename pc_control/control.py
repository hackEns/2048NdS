#!/usr/bin/env python2
# -*- coding: utf8 -*-

# All colors are in [0,255] but we have to send values between [0,127]
import colors
import time


class Control():
    def __init__(self, ser, nb_leds,
                 corrections={'r': 1.0, 'g': 1.0, 'b': 1.0},
                 brightness=1.0,
                 nb_steps_fading=15):
        # ser should be an opened pySerial object
        self.corrections = {k: brightness * corrections[k]
                            for k in corrections}
        self.ser = ser
        self.nb_leds = nb_leds
        self.nb_steps_fading = nb_steps_fading
        self.current_colors = [{'r': 255, 'g': 0, 'b': 0}
                               for i in xrange(nb_leds)]

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

    def send_color(self, id, color, duration=1, fading=False):
        """Corrects the color and send it over serial

        If fading is passed and is not false, interpolate to do a fading
        between current and dest color. Fading can be an int to bypass the
        default number of intermediate steps.
        duration is the total duration of the color (or the fading)
        """
        data = []
        if fading is not False:
            if isinstance(fading, (int, long)):
                steps = colors.fading(self.current_color[id],
                                      color,
                                      fading)
                wait = float(duration) / fading
            else:
                steps = colors.fading(self.current_color[id],
                                      color,
                                      self.nb_steps_fading)
                wait = float(duration) / self.nb_steps_fading
        else:
            steps = [color]

        for step in steps:
            data += [0x80 + id]
            data.extend(v for k, v in self.correct_color(step).iteritems())

        for i in xrange(len(data)):
            self.ser.write(chr(data[i]))
            if i % 4 == 0:
                time.sleep(wait)
        self.current_color[id] = color

    def send_colors(self, colors, duration=1, fading=False, starting=0):
        """Send the colors to all the LEDs

        params:
            colors is a list of color dicts
            starting is the index of the first LED to control
            fading, see send_color
            duration is the total duration of the color (or the fading)
        """
        if fading is not False:
            if isinstance(fading, (int, long)):
                steps = [colors.fading(self.current_color[id],
                                       colors[id],
                                       fading)
                         for id in xrange(len(colors))]
                wait = float(duration) / fading
            else:
                steps = [colors.fading(self.current_color[id],
                                       colors[id],
                                       self.nb_steps_fading)
                         for id in xrange(len(colors))]
                wait = float(duration) / self.nb_steps_fading
        else:
            steps = [[colors[id]] for id in xrange(len(colors))]
            wait = duration

        for k in xrange(len(steps[0])):
            for i in xrange(starting, min(self.nb_leds, len(colors)+starting)):
                self.send_color(i, steps[i][k], duration=0)
            time.sleep(wait)

    def reset(self):
        """Resets all the LEDs to red"""
        for k in range(self.nb_leds):
            for i in [0x80 + k, 127, 0, 0]:
                self.ser.write(chr(i))
