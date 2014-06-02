/* This code runs on the LEDs PCB and handles the serial communication and
 * correct colors display.
 *
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
#define R 0
#define G 1
#define B 2
const int pins[3] = {9, 10, 11};

void setup() {
    // Led R to show that microcontroller is ready
    analogWrite(pins[R], 255);
    analogWrite(pins[G], 0);
    analogWrite(pins[B], 0);
}

void loop() {
    // TODO
}
