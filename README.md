Nuit des Sciences 2014
======================

Codes, schematics etc. pour l'installation de LEDs (montage Ledhill) pour la Nuit des Sciences 2014 à l'Ens.

# Structure

* `frontend/`: web interface for playing, customized 2048 game to be used as a controller for the game server.
* `leds/`: code running on the ATmega on the LEDs PCB.
* `pc_control/`: python scripts to send instructions to the LEDs.
* `tests/`: various tests files for both the PCBs and the Serial comm in Python.

# Usage

* Launch `test_order.py` in the `tests` folder, to get the correct order in which LEDs should be controlled.
* Put the output of the previous command in the `get_linear_led_number` function in `pc_control/game.py` line 98 to set the correct order for the LEDs.
* Set the correct controller at the top of `pc_control/game.py`.
* Launch `leds_server.py` in the `pc_control` folder, on the computer connected to the LEDs using a USB FTDI cable. Pass the device `/dev/ttyUSB*` used to communicate with the LEDs as argument.
* Launch `game.py` in the `pc_control` folder passing it the server ip address as first argument. This can be launched on any computer as long as it can communicate with the previous one _via_ the port 4242 (or any other port, if you update the files `game.py` and `leds_server.py` accordingly).
* You are ready to go.

# License

All the source codes, unless explicitly specified otherwise are under the following license:

```
/*
 * --------------------------------------------------------------------------------
 * "THE NO-ALCOHOL BEER-WARE LICENSE" (Revision 42):
 * Phyks (webmaster@phyks.me) wrote or updated these files for hackEns. As long
 * as you retain this notice you can do whatever you want with this stuff
 * (and you can also do whatever you want with this stuff without retaining it,
 * but that's not cool...).
 *
 * If we meet some day, and you think this stuff is worth it, you can buy us a
 * <del>beer</del> soda in return.
 *                                                              Phyks for hackEns
 * ---------------------------------------------------------------------------------
 */
 ```
