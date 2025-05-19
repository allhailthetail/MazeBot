#!../../venv/bin/python3
# Add parent directory to sys.path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../python/')))
from PiBoe.chassis import BoeDriver

#print(sys.path)

def back_and_forth(Driver):
    Driver.foreward(sec = 2)
    Driver.reverse(sec = 2)


# Test various speed factors and yaw:
def main():
    # Initialize Driver for BOE Bot:
    Driver = BoeDriver()

    # Test out speeds 1-8:
    #    (just change range)
    for i in range(7,8):
        print(f"Testing for Speed: {i}")
        Driver._set_speed(newspeed = i)
        back_and_forth(Driver)

    # Test out yaw:
    Driver._set_speed(newspeed = 4)
    Driver.yaw(clockwise=True, sec=10)
    Driver.yaw(clockwise=False, sec=10)

    # Test out camera yaw:
    # Full right
    Driver.yaw_cam(deg_increment=90)
    # Full left
    Driver.yaw_cam(clockwise=False, deg_increment=180)
    # Reset to straight-ahead
    Driver.yaw_cam(reset=True)

if __name__ == "__main__":
    main()
