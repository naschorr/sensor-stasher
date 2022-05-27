# SHT31 Temperature and Humidity Sensor

## Hardware Setup
- VIN to 3.3v pin of your choice (For example, pin 17)
- GND to ground pin of your choice (For example, pin 14)
- SCL to pin 3 (I2C SCL)
- SDA to pin 2 (I2C SDA)

## Software Setup
- Configuration through `sudo raspi-config` (Is this necessary, can this be replaced by editing /boot/config.txt?):
    - Select "Interface Options"
    - Select "I2C"
    - Select "Yes" when asked about enabling the ARM I2C interface
    - Select "Ok" when asked to confirm your choices
    - Leave the configurator, then `sudo reboot`

~~- Make sure `dtoverlay=i2c-gpio` is present in `/boot/config.txt`, otherwise the i2c devices won't be available~~

## Notes
- Note that additional I2C ports can be opened, see here: https://medium.com/cemac/creating-multiple-i2c-ports-on-a-raspberry-pi-e31ce72a3eb2
- The sensor doesn't want to connect to the i2c bus after a `sudo reboot`, only after a physical power reset.
    - Specifically, when shorting 3.3v to ground on the SHT31's board.
