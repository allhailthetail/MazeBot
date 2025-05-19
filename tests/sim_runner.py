# Add parent directory to sys.path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../python')))

import pygame, math, gpiozero
from types import SimpleNamespace
from MazeBotML.env_and_robot import Envir, Robot
#from MazeBotML.sim_motor.py import SimWheelBase
from MazeBotML.sim_motor import SimWheelBase
from MazeBotML.line_follow import TapeFollower
from MazeBotML.graph_builder import MazeGraph
from MazeBotML.heading_utils import heading_lookup
from MazeBotML.line_follow import GPIO_LEFT, GPIO_RIGHT



robot = None
environment = None

def make_sensor(idx):
    return SimpleNamespace(value=robot.read_sensor(idx, environment.map))

# Disable real pins and replace DigitalInputDevice with lambda
gpiozero.Device.pin_factory = None
gpiozero.DigitalInputDevice = lambda pin: make_sensor(
    0 if pin == GPIO_LEFT else 1
) 

# Initializations
pygame.init()

# start position
start=(200,200)
dims=(600,1200)

# Running or not
running = True

# The environmnet
environment=Envir(dims)

# The robot
robot = Robot(start, 
              "../static/images/sampleBot.png",
              0.01*3779.52)

# Delta time
dt = 0
last_time = pygame.time.get_ticks()

# Simulation loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        robot.move(event) #TODO fix? move(self,dt)

    dt = (pygame.time.get_ticks() - last_time) / 1000 
    last_time = pygame.time.get_ticks()
    pygame.display.update()
    environment.map.fill(environment.black)
    robot.move()
    if hasattr(robot, "drive_until") and pygame.time.get_ticks() > robot.drive_until:
        robot.vl = robot.vr = 0
    environment.write_info(int(robot.vl),
                           int(robot.vr),
                           robot.theta)
    robot.draw(environment.map)
    environment.trail((robot.x, robot.y))
    environment.robot_frame((robot.x, robot.y), robot.theta)


