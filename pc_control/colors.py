#!/usr/bin/env python2
# -*- coding: utf8 -*-


def rgb255_to_hsv(color):
    """Converts a 3 bytes RGB color to HSV values.
    Conversion rules from:
        https://fr.wikipedia.org/wiki/Teinte_Saturation_Valeur

    params: color a {r, g, b} dict
    returns: a color dict
    """
    color = {k: color[k] / 255.0 for k in color}
    color_out = {'t': 0.0, 's': 0.0, 'v': 0.0}

    M = max([color[i] for i in color])
    m = min([color[i] for i in color])

    if m == M:
        color_out['t'] = 0.0
    elif M == color['r']:
        color_out['t'] = (60 * (color['g'] - color['b']) / M - m + 360) % 360
    elif M == color['g']:
        color_out['t'] = (60 * (color['b'] - color['r']) / M - m + 120)
    elif M == color['b']:
        color_out['t'] = (60 * (color['r'] - color['g']) / M - m + 240)

    if M == 0.0:
        color_out['s'] = 0.0
    else:
        color_out['s'] = 1 - m / M

    color_out['v'] = M

    return color_out


def hsv_to_rgb255(color):
    """Converts a HSV color to 3 bytes RGB color
    Conversion rules from:
        https://fr.wikipedia.org/wiki/Teinte_Saturation_Valeur

    params: color_tsv is a {h, s, v} dict
    returns: a color dict
    """
    qd = int(color['t'] / 60) % 6
    f = color['t'] / 60 - qd
    l = color['v'] * (1 - color['s'])
    m = color['v'] * (1 - f * color['s'])
    n = color['v'] * (1 - (1 - f) * color['s'])

    answer = [
        {'r': color['v'], 'g': n, 'b': l},
        {'r': m, 'g': color['v'], 'b': l},
        {'r': l, 'g': color['v'], 'b': n},
        {'r': l, 'g': m, 'b': color['v']},
        {'r': n, 'g': l, 'b': color['v']},
        {'r': color['v'], 'g': l, 'b': m},
    ]
    return {k: int(answer[qd][k] * 255) for k in answer[qd]}


def rgb255_to_rgb127(color):
    """Converts a RGB color indexed in [0,255] to one index in [0,127]"""
    return {'r': color['r'] >> 1, 'g': color['g'] >> 1, 'b': color['b'] >> 1}


def rgb127_to_rgb255(color):
    """Converts a RGB color indexed in [0,127] to one index in [0,255]"""
    return {'r': color['r'] << 1, 'g': color['g'] << 1, 'b': color['b'] << 1}
