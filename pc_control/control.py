#!/usr/bin/env python2
# -*- coding: utf8 -*-

# Parameters
corrections = {'r': 1.0, 'g': 1.0, 'b': 1.0}
brightness = 1.0
# ==========

corrections = {k: brightness * corrections[k] for k in corrections}


def get_corrected_color(color):
    """Corrects the color to match real LED render

    params: color a {r, g, b} dict
    returns: a color dict
    """
    return {i: color[i] * corrections[i] for i in color}


def send_color(id, color, ser):
    """Corrects the RGB127 color and send it over serial"""
    data = [0x80 + id]
    data.extend(v for k, v in get_corrected_color(color).iteritems())
    for i in data:
        ser.write(chr(i))
