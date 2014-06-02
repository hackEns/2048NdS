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
#
# This is a script to test animation and fading
# Usage: Edit the parameters section to fit your needs

import colors
import math
import matplotlib.pyplot as plt
import numpy as np
import predefined_colors
from matplotlib import animation


if __name__ == '__main__':
    # Parameters
    start_color = {'r': 255, 'g': 0, 'b': 0}
    end_color = {'r': 0, 'g': 0, 'b': 0}
    nb_leds = 9
    duration = 3
    filename = "output.mp4"
    # End

    iterations = 25 * duration
    size = int(math.sqrt(nb_leds) * 10 + (math.sqrt(nb_leds) - 1) * 2)

    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=25, bitrate=1800)

    fading = colors.fading(start_color, end_color, iterations)
    images = [np.zeros((size, size, 3), np.uint8) for _ in range(iterations)]

    count = 0
    for img in range(len(images)):
        for k in range(int(math.sqrt(nb_leds))):
            for l in range(int(math.sqrt(nb_leds))):
                for i in range(10):
                    for j in range(10):
                        images[img][i + k*12, j + l*12] = (fading[count]['r'],
                                                           fading[count]['g'],
                                                           fading[count]['b'])
        count += 1

    fig = plt.figure()
    im = plt.imshow(images[0], interpolation='nearest')

    def animate(i):
        im.set_array(images[i])
        return im,

    anim = animation.FuncAnimation(fig, animate, frames=duration * 25,
                                   interval=1000/25,
                                   blit=True)
    plt.show()
    anim.save(filename, writer=writer)
