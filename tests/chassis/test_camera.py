#!../../venv/bin/python3
# Add parent directory to sys.path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../python/')))
from PiBoe.chassis import BoeDriver

# Test camera:
def main():
    # Initialize Driver for BOE Bot:
    Driver = BoeDriver()

    # Max increment for one step:
    increment = 90

    # Full right in one increment:
    Driver.yaw_cam(deg_increment=90)
    # Full Left in 2 increments:
    Driver.yaw_cam(clockwise=False, deg_increment=increment)
    Driver.yaw_cam(clockwise=False, deg_increment=increment)

    # Reset to straight-ahead (regardless of increment)
    Driver.yaw_cam(reset=True)

if __name__ == "__main__":
    main()
