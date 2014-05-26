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

import colors
import serial
import time
import tools


class Control():
    """Class to control the LEDs by sending instructions over serial.

    All colors are RGB in [0,255] but we have to send values between [0,127]
    to the LEDs.
    """
    def __enter__(self):
        return self

    def __init__(self, serial_port, nb_leds,
                 corrections={'r': 1.0, 'g': 1.0, 'b': 1.0},
                 brightness=1.0,
                 nb_steps_fading=25):
        """Params:
            * ser is an open pySerial object
            * nb_leds is the total number of LEDs
            * corrections is used to correct the differences between colors
            intensity
            * brightness is used to reduce the global brightess
            * nb_steps_fading is the number of steps to use by default for
            fading
        """
        self.corrections = {k: float(brightness) * corrections[k]
                            for k in corrections}

        self.serial_port = serial_port
        self.ser = serial.Serial(port=self.serial_port, baudrate=115200)
        if not self.ser.isOpen():
            try:
                self.ser.open()
            except Exception, e:
                tools.error("Error opening serial port: " + str(e))
        if not self.ser.isOpen():
            tools.error("Serial port not opened")
        self.ser.flushInput()
        self.ser.flushOutput()

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
        return {i: int(color[i] * self.corrections[i]) >> 1 for i in color}

    def send_color(self, id, color, fading=False, fading_duration=1):
        """Corrects the color and send it over serial

        Params:
            * id is the id of the LED to address
            * color is a RGB255 color dict
            * fading_duration is the total duration of the fading

        If fading is passed and is not false, interpolates to do a fading
        between current and dest color. Fading can be an int to bypass the
        default number of intermediate steps or just True.
        """
        data = []
        if fading is not False:
            if isinstance(fading, (int, long)):
                steps = colors.fading(self.current_colors[id],
                                      color,
                                      fading)
                wait = float(fading_duration) / fading
            else:
                steps = colors.fading(self.current_colors[id],
                                      color,
                                      self.nb_steps_fading)
                wait = float(fading_duration) / self.nb_steps_fading
        else:
            steps = [color]
            wait = 0

        for step in steps:
            data += [0x80 + id]
            data.extend(v for k, v in self.correct_color(step).iteritems())

        for i in xrange(len(data)):
            self.ser.write(chr(data[i]))
            if i % 4 == 0:
                time.sleep(wait)
        self.current_colors[id] = color

    def send_colors(self, colors, starting=0, fading=False, fading_duration=1):
        """Send colors instruction to a bunch of LEDs

        Params:
            * colors is a list of color dicts for each LEDs
            * starting is the index of the first LED to control
            * fading, see send_color()
            * fading_duration is the total duration of the fading
        """
        if fading is not False:
            if isinstance(fading, (int, long)):
                steps = {int(id): colors.fading(self.current_colors[id],
                                                colors[id],
                                                fading)
                         for id in colors}
                wait = float(fading_duration) / fading
            else:
                steps = {int(id): colors.fading(self.current_colors[id],
                                                colors[id],
                                                self.nb_steps_fading)
                         for id in colors}
                wait = float(fading_duration) / self.nb_steps_fading
        else:
            steps = {int(id): [colors[id]] for id in colors}
            wait = 0

        for k in xrange(len(steps[steps.iterkeys().next()])):
            for i in steps:
                # Send the color to the individual LED, and duration is 0 as
                # it is handled inside this function (globally and not per LED)
                if i + starting > self.nb_leds:
                    continue  # No need to send useless data
                self.send_color(i + starting, steps[i][k], fading_duration=0)
            time.sleep(wait)

    def reset(self):
        """Resets all the LEDs to red, default state after setup()"""
        for k in range(self.nb_leds):
            for i in [0x80 + k, 127, 0, 0]:
                self.ser.write(chr(i))

    def close(self):
        """Closes the serial communication"""
        if self.ser.isOpen():
            self.ser.close()

    def __exit__(self, type, value, traceback):
        self.close()
