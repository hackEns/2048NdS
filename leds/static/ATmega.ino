
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
#include <math.h>
#define R 0
#define G 1
#define B 2

struct RGBColor {
    int r;
    int g;
    int b;
};

struct RGBColorFloat {
    float r;
    float g;
    float b;
};

struct HSVColor {
    float h;
    float s;
    float v;
};

const struct RGBColor red = {255, 0, 0};
const struct RGBColor rose = {232, 30, 116};
const struct RGBColor black = {0, 0, 0};
const struct RGBColorFloat corrections = {1, 1, 1};
const int pins[3] = {9, 10, 11};


struct HSVColor rgb255_to_hsv(struct RGBColor color_in) {
    RGBColorFloat color = {float(color_in.r) / 255, float(color_in.g) / 255, float(color_in.b) / 255};
    HSVColor color_out = {0, 0, 0};

    float M = max(color.r, max(color.g, color.b));
    float m = min(color.r, min(color.g, color.b));

    if(m == M) {
        color_out.h = 0.0;
    }
    else if(M == color.r) {
        color_out.h = fmod(60 * (color.g - color.b) / M - m + 360, 360);
    }
    else if(M == color.g) {
        color_out.h = (60 * (color.b - color.r) / M - m + 120);
    }
    else if(M == color.b) {
        color_out.h = (60 * (color.r - color.g) / M - m + 240);
    }

    if(M == 0.0) {
        color_out.s = 0.0;
    }
    else {
        color_out.s = 1 - m / M;
    }

    color_out.v = M;

    return color_out;
}


RGBColor hsv_to_rgb255(HSVColor color) {
    int qd = int(color.h / 60) % 6;
    float f = color.h / 60 - qd;
    float l = color.v * (1 - color.s);
    float m = color.v * (1 - f * color.s);
    float n = color.v * (1 - (1 - f) * color.s);
    RGBColor color_out = {0, 0, 0};

    switch(qd) {
        case 0:
            color_out.r = 255*color.v;
            color_out.g = 255*n;
            color_out.b = 255*l;
            break;

        case 1:
            color_out.r = 255*m;
            color_out.g = 255*color.v;
            color_out.b = 255*l;
            break;

        case 2:
            color_out.r = 255*l;
            color_out.g = 255*color.v;
            color_out.b = 255*n;
            break;

        case 3:
            color_out.r = 255*l;
            color_out.g = 255*m;
            color_out.b = 255*color.v;
            break;

        case 4:
            color_out.r = 255*n;
            color_out.g = 255*l;
            color_out.b = 255*color.v;
            break;

        case 5:
            color_out.r = 255*color.v;
            color_out.g = 255*l;
            color_out.b = 255*m;
            break;
    }
    return color_out;
}


void show_color(RGBColor color) {
    analogWrite(pins[R], (int) (color.r * corrections.r));
    analogWrite(pins[G], (int) (color.g * corrections.g));
    analogWrite(pins[B], (int) (color.b * corrections.b));
}


void fading(RGBColor src_color, RGBColor dest_color, int nb_steps) {
    HSVColor src_color_hsv = rgb255_to_hsv(src_color);
    HSVColor dest_color_hsv = rgb255_to_hsv(dest_color);
    HSVColor current_color = {0, 0, 0};

    float step_size_h = float(dest_color_hsv.h - src_color_hsv.h) / nb_steps;
    float step_size_s = float(dest_color_hsv.s - src_color_hsv.s) / nb_steps;
    float step_size_v = float(dest_color_hsv.v - src_color_hsv.v) / nb_steps;

    for(int i = 0; i < nb_steps + 1; ++i) {
        current_color.h = src_color_hsv.h + i * step_size_h;
        current_color.s = src_color_hsv.s + i * step_size_s;
        current_color.v = src_color_hsv.v + i * step_size_v;
        show_color(hsv_to_rgb255(current_color));
        delay(40);
    }
}


void setup() {
    show_color(red);
    randomSeed(analogRead(0));
    delay(1000);
    show_color(black);
}

void loop() {
    int rand_fading_duration = random(60);
    int rand_duration = random(60, 180);

    fading(black, rose, 25*rand_fading_duration);
    delay(rand_duration*1000);
    rand_fading_duration = random(60);
    fading(rose, black, 25*rand_fading_duration);
    rand_duration = random(60, 180);
    delay(rand_duration*1000);
}
