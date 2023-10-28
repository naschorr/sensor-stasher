# PMS7003 Particulate Matter Sensor

## Software Setup
- Make sure `enable_uart=1` is set in `/boot/config.txt`, otherwise the serial devices won't be available
- Configuration through `sudo raspi-config` (Is this necessary, can this be replaced by editing /boot/config.txt?):
    - Select "Interface Options"
    - Select "Serial Port"
    - Select "No" when asked about a login shell being accessible over serial
    - Select "Yes" when asked about enabling the serial port hardware
    - Select "Ok" when asked to confirm your choices
    - Leave the configurator, then `sudo reboot`
