# Build a maze (In real life with black tape)

"""
Assumes two digital reflectance sensors:
- left_sensor GPIO 23
- right_sensor GPIO 24

When a sensor sees Black tape -> it reads LOW(0)
When it sees White floor -> it reads HIGH(1)
"""

from gpiozero import DigitalInputDevice
import time

# Tunable constants 
GPIO_LEFT = 23
GPIO_RIGHT = 24
BASE_SPEED = 0.35 
Kp = 0.25 # proportional gain
EDGE_GAP_MS = 120

# Class to follow the lines and avoid Black Tape
class TapeFollower:
    def __init__(self, wheelbase):
        self.wb = wheelbase
        self.sL = DigitalInputDevice(GPIO_LEFT)
        self.sR = DigitalInputDevice(GPIO_RIGHT)
        self.last_black_ms = int(time.time()*1000)
        self.white_count = 0
    
    def _read_err(self):
        """
        Returns -1 0 +1:
        - -1 tape under right only -> need to steer right
        - 1 tape under left only -> need to steer left
        - 0 both sensors same -> on track or gap
        """

        l = int(not self.sL.value) # invert: 1 = black
        r = int(not self.sR.value)
        return l - r
    
    def step(self):
        """
        One control-loop iteration.
        Drives the wheels for approx. 10 ms and returns 
            True if it thinks we hit a junction (big white patch)
            False otherwise
        """
        now = int(time.time()*1000)
        err = self._read_err()
        print(f"L={self.sL.value}  R={self.sR.value}  err={err}") 
        

        # Juction detection
        if err == 0 and self.sL.value and self.sR.value:
            # if Both are white for EDGE_GAP_MS => probably a junction
            #print("[SENS]  both-white timer passed")
            self.white_count += 1
            # Else it's still on the tape
        else:
            self.white_count = 0
            self.last_black_ms = now
        
        if self.white_count > 3 and now - self.last_black_ms > EDGE_GAP_MS:
            self.white_count = 0
            self.wb.stop()
            return True
                
        if hasattr(self.wb, "ignore_junction_until") and now < self.wb.ignore_junction_until:
            pass
        # P controller
        left_cmd = BASE_SPEED - Kp*err
        right_cmd = BASE_SPEED + Kp*err
        self.wb.drive(left_cmd, right_cmd)
        #print(f"[SENS]  drive L={left_cmd:.2f} R={right_cmd:.2f}")
        return False
    