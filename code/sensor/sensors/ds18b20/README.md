# DS18B20 Temperature Sensor

## Pinout
- Red: 3.3v
- Yellow: Data
- Black: Ground

## Hardware Setup
- Put a 4.7 kOhm or 10 kOhm resistor between 3.3v and data wires
- Red goes to pin 1
- Yellow goes to pin 7 (GPIO 4), since this is the default GPIO pin for one-wire communication. If desired, other GPIO pins can be used instead with some minor configuration tweaks. Read about that [here](https://pinout.xyz/pinout/1_wire#).
- Black goes to pin 9

## Software Setup
1. Enable the one wire overlay by adding `dtoverlay=w1-gpio` to the bottom of your `/boot/config.txt` file
1. Reboot with `sudo reboot`
1. After the reboot, enable the kernel modules for the one wire interface
    - `sudo modprobe w1-gpio` (nothing will happen)
    - `sudo modprobe w1-therm` (nothing will happen)
1. Navigate to the sensor's device directory: `cd /sys/bus/w1/devices/28-*`
1. Read the raw data: `cat w1_slave`. You'll see something like:
    ```
    7a 01 4b 46 7f ff 06 10 0b : crc=0b YES
    7a 01 4b 46 7f ff 06 10 0b t=23625
    ```
    where `t=23625` is the output in celcius (without the decimal). In this case, it's currently a slightly warm 23.625 degrees celcius.
