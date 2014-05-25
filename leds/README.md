Code sur les ATmega
====

Some notes on the PCBs and the code:

## Pins

* 15 (datasheet ATmel) == 9 (Arduino) : Led R
* 16 (datasheet ATmel) == 10 (Arduino) : Led G
* 17 (datasheet ATmel) == 11 (Arduino) : Led B

## Serial packets

A serial packet is as follow (4 bytes):

```
synchro (= 1) | function |  counter
 1bit         |  1 bit   |  6 bits
```

```
synchro (= 0) |  colorR
 1bit         |  7 bits
```

```
synchro (= 0) |  colorG
 1bit         |  7 bits
```

```
synchro (= 0) |  colorB
 1bit         |  7 bits
```

## Functions

* `0b0` : Immediate switch
* `0b1` : Broadcast (treat the packet but still forward it with null counter)

## Misc

* serialEvent is automatically called at the end of `loop()` if data is available on RX.
* When a header arrives, `serial_i = counter`
* `serial_i` describes the state:
    * `-1` => waiting for a header packet
    * `0` => waiting for data for red LED
    * `1` => waiting for data for blue LED
    * `2` => waiting for data for green LED
* No need to call `pinMode` before an `analogWrite`
