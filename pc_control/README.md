PC Control of the LED for the 2048-like installation
====================================================

This is the code to run on the PC to control the LEDs.

It is composed of two modules:
* A game server `game.py` to handle the game and forge instructions for the LEDs.
* A LED server `leds_server.py` which waits for instructions and send them to the LEDs.

Both of them communicate _via_ the network. You should edit parameters in caps in the two previous files to match your configuration.

The game server uses a game controller to get events and update its status. These are located in `game_controllers/`. The most basic one is `KeyboardController` which simply listen for keypress on the arrow keys. It can be used as an example for more sophisticated one.

## Usage

1. Launch the LED server: `./leds_server.py SERIAL_PORT` where `SERIAL_PORT` is the one used to communicate with the LEDs.
2. Launch the game server: `./game.py HOST` where `HOST` is the host for the LED server.
3. Play


## Available controllers

Edit the `game.py` file to use the controller you want. By default, it uses the `KeyboardController`.

Available controllers are:
* `KeyboardController()` to control the game using the keyboard (and the arrow keys) on the game server.
* `WebController()` to display the 2048 web interface and control the game directly in the browser.


## License

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

