#!../venv/bin/python3

import time
import pdb
from adafruit_servokit import ServoKit

# CONSTANT VARS:
DEF_SEC = 1.0    # Only allow bot to move for 0.5 sec if not specified...
DEF_CAM_ANGLE = 90

class BoeDriver:

    # Define which pins on the servo HAT the servos live at:
    left_pin = 0     # both continuous rotation...
    right_pin = 1
    camera_pin = 2   # standard servo

    # Structure: speed_value: [left_corr, right_corr, approx m/s] <-- TODO
    #    These likely need to be calculated manually...

    SPEED_FACTORS = {1: [0.034, 0.020],
                     2: [0.066, 0.050],
                     3: [0.110, 0.070]}

    def __init__(self):
        '''
        Initial values for the boe_driver class...
        '''

        # Assuming a 16-ch board, though 8ch is an option, also.
        self.kit = ServoKit(channels=16)

        self.speed = 1      #Default speed
        self.latency = 1.0  #Latency: wait between executing moves.
        self.def_sec = 0.5      #Unless otherwise noted, move for 1sec.

        self.camera_angle = 0
        self.yaw_speed = 10   #Default angle increment for camera

        # Look straight ahead on init:
        self._set_cam_angle(self.camera_angle)

    def _set_speed(self, newspeed):
        '''
        Define a new speed for motion:
        '''
        if newspeed in self.SPEED_FACTORS.keys():
            self.speed = newspeed
        else:
            print("ERR, newspeed is out of scope... Check SPEED_FACTORS...")
            pass

    def _set_cam_angle(self, deg):
        '''
        Define yaw angle for the camera:
        kit.servo.angle <- Appropriate method for normal servos
        '''

        current_pos = self.camera_angle
        # (-)Clockwise/right (+)Counter-Clockwise/left
        if deg < -90 or deg > 90:
            print(f"Current Angle: {current_pos}, New Angle {deg} out of range, ignoring request...")
            pass

        else:
            # Assign new value to camera_angle and rotate:
            self.camera_angle = deg
            self.kit.servo[self.camera_pin].angle = self.camera_angle + DEF_CAM_ANGLE

    def _all_stop(self):
        '''
        Call all stop at end of every motion function...
        '''
        self.kit.continuous_servo[self.left_pin].throttle = 0
        self.kit.continuous_servo[self.right_pin].throttle = 0

        # Wait time after executing a move...
        time.sleep(self.latency)

    def foreward(self, sec=None):
        '''
        Define foreward motion for the bot:
        kit.continuous_servo.throttle <- Appropriate method for continuous rotation servos
        '''

        # If user fails to specify, only move by globally static value.
        if sec == None:
            sec = DEF_SEC

        # Left control...
        left_speed = self.SPEED_FACTORS[self.speed][self.left_pin]
        self.kit.continuous_servo[self.left_pin].throttle = left_speed

        # Right Control
        right_speed = -1 * self.SPEED_FACTORS[self.speed][self.right_pin]
        self.kit.continuous_servo[self.right_pin].throttle = right_speed

        # Travel for...
        time.sleep(sec)

        # Always stop the bot as last step of function:
        self._all_stop()

    def reverse(self, sec=None):
        '''
        Define reversemotion for the bot:
        kit.continuous_servo.throttle <- Appropriate method for continuous rotation servos
        '''

        # If user fails to specify, only move by globally static value.
        if sec == None:
            sec = DEF_SEC

        # Left control...
        left_speed = -1 * self.SPEED_FACTORS[self.speed][self.left_pin]
        self.kit.continuous_servo[self.left_pin].throttle = left_speed

        # Right Control
        right_speed = self.SPEED_FACTORS[self.speed][self.right_pin]
        self.kit.continuous_servo[self.right_pin].throttle = right_speed

        # Travel for...
        time.sleep(sec)

        # Always stop the bot as last step of function:
        self._all_stop()

    def yaw(self, clockwise=True, sec=None):
        '''
        Define yaw for the bot:
        (Assume clockwise...)
        kit.continuous_servo.throttle <- Appropriate method for continuous rotation servos
        '''

        # If user fails to specify, only move by globally static value.
        if sec == None:
            sec = DEF_SEC

        # Yaw CCW behavior:
        if clockwise == False:
            # Left control...
            left_speed = -1 * self.SPEED_FACTORS[self.speed][self.left_pin]
            self.kit.continuous_servo[self.left_pin].throttle = left_speed

            # Right Control
            right_speed = -1 * self.SPEED_FACTORS[self.speed][self.right_pin]
            self.kit.continuous_servo[self.right_pin].throttle = right_speed

            # Travel for...
            time.sleep(sec)

        # Yaw CW behavior:
        else:
            # Left control...
            left_speed = self.SPEED_FACTORS[self.speed][self.left_pin]
            self.kit.continuous_servo[self.left_pin].throttle = left_speed

            # Right Control
            right_speed = self.SPEED_FACTORS[self.speed][self.right_pin]
            self.kit.continuous_servo[self.right_pin].throttle = right_speed

            # Travel for...
            time.sleep(sec)

        # Always stop the bot as last step of function:
        self._all_stop()

    def yaw_cam(self, clockwise=True, deg_increment=None, reset=False):
        '''
        Incrementally yaws the camera by a set angle.
        Relies on _set_cam_angle to avoid out of bounds conditions.
        reset=True will always reset camera to default pos, regardless of other inputs.
        '''

        # Reset camera position to default...
        if reset:
            self._set_cam_angle(deg=0)
            return

        # Default to default yaw speed if none specified
        if deg_increment == None:
            deg_increment = self.yaw_speed

        if clockwise == True:
            self._set_cam_angle(-1 * deg_increment + self.camera_angle)
        elif clockwise == False:
            self._set_cam_angle(deg_increment + self.camera_angle)
        else:
            print("DEBUG: yaw_cam undefined behavior...")
            pass

        time.sleep(self.latency)

def main():
    # Instantiate the bot driver:
    Driver = BoeDriver()

    print("Welcome to Driver Interactive Console...\n\n")
    pdb.set_trace()

    # Example Code:
    #    Driver._set_speed(newspeed= 3)
    #    Driver.foreward(sec= 5)
    #    Driver.reverse(sec= 5)
    #    Driver.yaw(sec= 10)
    #    Driver.yaw(clockwise= False, sec= 10)

if __name__ == "__main__":
    main()
