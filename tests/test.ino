// Arduino sketch to test the LEDs
// Will blink Green / Red / Blue
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


void setup() {
    pinMode(9, OUTPUT);
    pinMode(10, OUTPUT);
    pinMode(11, OUTPUT);
    digitalWrite(9, HIGH);
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);
}

void loop() {
    digitalWrite(9, LOW);
    digitalWrite(10, HIGH);

    delay(500);

    digitalWrite(10, LOW);
    digitalWrite(11, HIGH);

    delay(500);

    digitalWrite(11, LOW);
    digitalWrite(9, HIGH);

    delay(500);
}
