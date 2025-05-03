from gpiozero import Servo
import time

class WheelBase:
    def __init__(self, 
                 left_pin=18,
                 right_pin=19,
                 min_pw=0.5/1000, 
                 max_pw=2.5/1000):
        self.left = Servo(left_pin, min_pw, max_pw)
        self.right = Servo(right_pin, min_pw, max_pw)
    
    def drive(self, speed_left, speed_right, dur=None):
        """Speed between -1 and 1. Duration in seconds."""
        self.left.value = speed_left
        self.right.value = speed_right
        if dur:
            time.sleep(dur)
            self.stop()
    
    def stop(self):
        self.left.value = self.right.value = 0
    
