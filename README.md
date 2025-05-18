# boenanna-pi
Raspberry Pi controlling a BOE Bot chassis

[Chassis Driver Demonstration](https://youtu.be/iw_Xe_JajT4?si=0qx1W1s7F3d5nseO)

[3D-printed Base](https://www.thingiverse.com/thing:1562194)

# rpi prep:
- Install rpi minimal
- Enable ssh
- Enable I2C
- Connect 16-channel servo to board
- Connect servos to appropriate slots (check that they match scripts 0,1,2...)

# Installation:
> Project uses a virtual environment...

``` shell
python3 -m venv venv #Inside this dir.
source ./venv/bin/activate

pip install -r requirements.txt
```

