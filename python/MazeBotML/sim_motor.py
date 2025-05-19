import pygame

class SimWheelBase():
    def __init__(self, sim_robot):
        self.robot = sim_robot
    
    def drive(self, speed_left, speed_right, dur=None):
        self.robot.vl = speed_left * self.robot.maxspeed
        self.robot.vr = speed_right * self.robot.maxspeed
        if dur: 
            self.robot.drive_until = (
                pygame.time.get_ticks() + int(dur*1000)
            )
    
    def stop(self):
        self.robot.vl = self.robot.vr = 0