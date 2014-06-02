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

#define SERIAL_SPEED 115200

int serial_i = -1;
byte incoming_byte;

void setup() {
    Serial.begin(SERIAL_SPEED);

    // Led R to show that microcontroller is ready
    analogWrite(pins[R], 255);
    analogWrite(pins[G], 0);
    analogWrite(pins[B], 0);
}

void loop() {
    if(Serial.available()) {
        incoming_byte = (byte) Serial.read();

        // Header
        if(incoming_byte & B10000000) {
            serial_i = incoming_byte & B00111111;

            // Forward avec décrément du compteur
            if(serial_i != 0) {
                Serial.write(incoming_byte - 1);
                serial_i = -1;
            }

            // Broadcast
            if((incoming_byte & B01000000) == B01000000) {
                Serial.write(B11000000);
            }
        }
        // Paquet de couleur
        else {
            if(serial_i != -1) {
                analogWrite(pins[serial_i], incoming_byte << 1);
                serial_i++;
            }
            else {
                Serial.write(incoming_byte);
            }
        }
    }
}
