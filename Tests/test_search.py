import gpiozero
from gpiozero.pins.mock import MockFactory, MockPin 
from ..Python.motor_driver import WheelBase
from ..Python.line_follow import TapeFollower
from ..Python.graph_builder import MazeGraph

# Monkey-patch gpiozero to "pretend" it's connected to a pi
gpiozero.Device.pin_factory = MockFactory()

# Fake wheelbase
wb = WheelBase()

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
