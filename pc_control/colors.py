# -*- coding: utf8 -*-

# The functions in this file handle conversion between different color spaces
# and fading.

# -----------------------------------------------------------------------------
# "THE NO-ALCOHOL BEER-WARE LICENSE" (Revision 42):
# Phyks (webmaster@phyks.me) wrote or updated these files for hackEns. As long
# as you retain this notice you can do whatever you want with this stuff
# (and you can also do whatever you want with this stuff without retaining it,
# but that's not cool...).
#
# If we meet some day, and you think this stuff is worth it, you can buy us a
# <del>beer</del> soda in return.
#                                                        Phyks for hackEns
# -----------------------------------------------------------------------------


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
        color_out['h'] = 0.0
    elif M == color['r']:
        color_out['h'] = (60 * (color['g'] - color['b']) / M - m + 360) % 360
    elif M == color['g']:
        color_out['h'] = (60 * (color['b'] - color['r']) / M - m + 120)
    elif M == color['b']:
        color_out['h'] = (60 * (color['r'] - color['g']) / M - m + 240)

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
    qd = int(color['h'] / 60) % 6
    f = color['h'] / 60 - qd
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


def fading(src_color, dest_color, nb_steps):
    """Returns a list of steps colors to interpolate between src_color and
    dest_color (both RGB255) with a nb_steps steps fading"""
    src_color_hsv = rgb255_to_hsv(src_color)
    dest_color_hsv = rgb255_to_hsv(dest_color)

    step_size_h = float(dest_color_hsv['h'] - src_color_hsv['h']) / nb_steps
    step_size_s = float(dest_color_hsv['s'] - src_color_hsv['s']) / nb_steps
    step_size_v = float(dest_color_hsv['v'] - src_color_hsv['v']) / nb_steps

    return [hsv_to_rgb255({'h': src_color_hsv['h'] + i*step_size_h,
                           's': src_color_hsv['s'] + i*step_size_s,
                           'v': src_color_hsv['v'] + i*step_size_v})
            for i in xrange(1, nb_steps + 1)]
