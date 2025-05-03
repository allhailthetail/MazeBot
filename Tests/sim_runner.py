import pygame, math, gpiozero
from types import SimpleNamespace
from env_and_robot import Envir, Robot
from Maze import SimWheelBase
from ..Python.line_follow import TapeFollower
from ..Python.graph_builder import MazeGraph
from ..Python.heading_utils import heading_lookup



robot = None
environment = None

def make_sensor(idx):
    return SimpleNamespace(value=robot.read_sensor(idx, environment.map))

# Disable real pins and replace DigitalInputDevice with lambda
gpiozero.Device.pin_factory = None
from ..Python.line_follow import GPIO_LEFT, GPIO_RIGHT
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
              r"C:\Users\Utente\OneDrive\Desktop\Maze Bot\Bot Images\sampleBot.png",
              0.01*3779.52)

# Delta time
dt = 0
last_time = pygame.time.get_ticks()

# Simulation loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        robot.move(event)

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


