from types import SimpleNamespace
from env_and_robot import MAZE_EDGES, MAZE_JUNCTIONS
import pygame, math, gpiozero
import Python.line_follow as lf
from gpiozero.pins.mock import MockFactory
from Python.line_follow import GPIO_LEFT, GPIO_RIGHT

gpiozero.Device.pin_factory = MockFactory()

class SimSensor:
    def __init__(self, idx):
        self.idx = idx

    @property
    def value(self):
        # Dinamyc
        val = robot.read_sensor(self.idx, environment.map)
        print(f"[SIMSENSOR] idx={self.idx} → value={val}")
        return val

gpiozero.DigitalInputDevice = lambda pin: SimSensor(
    0 if pin == 23 else 1
)

lf.DigitalInputDevice = (
    lambda pin: SimSensor(0 if pin == GPIO_LEFT else 1)
)

from env_and_robot import Envir, Robot
from Python.sim_motor import SimWheelBase
from Python.line_follow import TapeFollower
from Python.graph_builder import MazeGraph
from Python.heading_utils import heading_lookup
import Python.sim_tag_reader as tagr
import Python.sim_main as main


# Build environment and robot
pygame.init()
dims = (600, 1200)
environment = Envir(dims)
environment.map.fill(environment.white)
environment.draw_maze()
robot = Robot(startpos=MAZE_JUNCTIONS[1], robotImg=r"C:\Users\Utente\OneDrive\Desktop\Maze_Bot\Bot Images\sampleBot.png",
              width=0.01*3779.52)

print_sensor = True

print("Sim pins ready:",
      gpiozero.DigitalInputDevice(GPIO_LEFT).value,
      gpiozero.DigitalInputDevice(GPIO_RIGHT).value)

# Virtual tag reader
tagr.init(robot, environment)

# Needed objects
wb = SimWheelBase(robot)
tf = TapeFollower(wb)
maze = MazeGraph()
controller = main.main_loop(wb, tf, maze, tagr.read_id) # generator

# Pygame loop
running, dt = True, 0
last = pygame.time.get_ticks()
while running:
    environment.map.fill(environment.white)
    environment.draw_maze()

    try:
        next(controller)
    except StopIteration:
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics time step
    now = pygame.time.get_ticks()
    dt = (now - last) / 1000
    last = now
    if hasattr(robot, "drive_until") and pygame.time.get_ticks() > robot.drive_until:
        robot.vl = robot.vr = 0
    robot.move(dt)

    

    # Draw
    environment.write_info(int(robot.vl), int(robot.vr), robot.theta)
    #environment.draw_sensors(robot, environment.map)
    robot.draw(environment.map)
    environment.trail((robot.x, robot.y))
    environment.robot_frame((robot.x, robot.y), robot.theta)
    # DEBUG sensor pixels
    lpx = int(robot.x + robot.sensor_offset[0][0]*math.cos(robot.theta)
            - robot.sensor_offset[0][1]*math.sin(robot.theta))
    lpy = int(robot.y - robot.sensor_offset[0][0]*math.sin(robot.theta)
            - robot.sensor_offset[0][1]*math.cos(robot.theta))
    rpx = int(robot.x + robot.sensor_offset[1][0]*math.cos(robot.theta)
            - robot.sensor_offset[1][1]*math.sin(robot.theta))
    rpy = int(robot.y - robot.sensor_offset[1][0]*math.sin(robot.theta)
            - robot.sensor_offset[1][1]*math.cos(robot.theta))

    print(f"SENSORS AT: L=({lpx},{lpy}) → {environment.map.get_at((lpx,lpy))}, "
        f"R=({rpx},{rpy}) → {environment.map.get_at((rpx,rpy))}")
    pygame.display.update()
pygame.quit()


