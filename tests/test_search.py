#!../venv/bin/python3
# Add parent directory to sys.path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../python')))

import gpiozero
from gpiozero.pins.mock import MockFactory, MockPin 
from MazeBotML.line_follow import TapeFollower
from MazeBotML.graph_builder import MazeGraph

from MazeBotML.motor_driver import WheelBase #TODO replace with PiBoe driver

# Monkey-patch gpiozero to "pretend" it's connected to a pi
gpiozero.Device.pin_factory = MockFactory()

# Fake wheelbase
wb = WheelBase() #TODO replace with PiBoe Driver...

# Feed canned sensor + tag events
tf = TapeFollower(wb)
maze = MazeGraph()

def test_short_maze():
    # fake sensors: right over black tape
    MockPin(23).state = 0
    MockPin(24).state = 1
    tf.step()
    # pretend we hit junction + tag 2
    maze.add_tag(1)
    maze.add_tag(2)
    path = maze.shortest(1,2)
    assert path == [1,2]
