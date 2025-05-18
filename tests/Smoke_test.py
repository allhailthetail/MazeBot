from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
kit.continuous_servo[0].throttle = +0.5   # spin wheel 0 forward
kit.continuous_servo[1].throttle = -0.5   # spin wheel 1 backward
time.sleep(1)
kit.continuous_servo[0].throttle = 0
kit.continuous_servo[1].throttle = 0