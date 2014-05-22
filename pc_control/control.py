# -*- coding: utf8 -*-

# Class to control the LEDs.

# All colors are RGB in [0,255] but we have to send values between [0,127] to the
# LEDs.
import colors
import time


class Control():
    def __init__(self, ser, nb_leds,
                 corrections={'r': 1.0, 'g': 1.0, 'b': 1.0},
                 brightness=1.0,
                 nb_steps_fading=15):
        """Params:
            * ser is an open pySerial object
            * nb_leds is the total number of LEDs
            * corrections is used to correct the differences between colors
            intensity
            * brightness is used to reduce the global brightess
            * nb_steps_fading is the number of steps to use by default for
            fading
        """
        self.corrections = {k: brightness * corrections[k]
                            for k in corrections}
        self.ser = ser
        self.nb_leds = nb_leds
        self.nb_steps_fading = nb_steps_fading
        self.current_colors = [{'r': 255, 'g': 0, 'b': 0}
                               for i in xrange(nb_leds)]

    def get_current_colors(self, id=None):
        """Returns the current colors of the LEDs, as a list"""
        if id is None:
            return self.current_colors
        else:
            return self.current_colors[id]

    def correct_color(self, color):
        """Corrects the color to match real LED render, applying `corrections`

        params: color a {r, g, b} dict
        returns: a color dict
        """
        return {i: color[i] * self.corrections[i] >> 1 for i in color}

    def send_color(self, id, color, duration=1, fading=False):
        """Corrects the color and send it over serial

        Params:
            * id is the id of the LED to address
            * color is a RGB255 color dict
            * duration is the total duration of the color (or the fading)

        If fading is passed and is not false, interpolates to do a fading
        between current and dest color. Fading can be an int to bypass the
        default number of intermediate steps or just True.
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

    def send_colors(self, colors, duration=1, starting=0, fading=False):
        """Send colors instruction to a bunch of LEDs

        Params:
            * colors is a list of color dicts for each LEDs
            * duration is the total duration of the color (or the fading)
            * starting is the index of the first LED to control
            * fading, see send_color()
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
                # Send the color to the individual LED, and duration is 0 as
                # it is handled inside this function (globally and not per LED)
                self.send_color(i, steps[i][k], duration=0)
            time.sleep(wait)

    def reset(self):
        """Resets all the LEDs to red, default state after setup()"""
        for k in range(self.nb_leds):
            for i in [0x80 + k, 127, 0, 0]:
                self.ser.write(chr(i))
