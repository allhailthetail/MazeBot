#TODO Integrate with chassis library.
from adafruit_servokit import ServoKit
import time, math
from env_and_robot import MAZE_JUNCTIONS, MAZE_EDGES
from Python.MyGraph import MyGraph

# Create the graph and calculate the best path (My Dijkstra)
# Configure nodes based on the maze
start_node = 6
goal_node = 19

# Build the graph and compute shortest path
G = MyGraph()
# Add weights (euclidean distances)
for u, v in MAZE_EDGES:
    x1, y1 = MAZE_JUNCTIONS[u]
    x2, y2 = MAZE_JUNCTIONS[v]
    dist = math.hypot(x2 - x1, y2 - y1)
    G.add_edge(u, v, weight=dist)
    

node_path = G.shortest_path(start=start_node, target=goal_node) # The output is something of the form [1, 2, 5]
path_length_mine = G.path_length(node_path)

# Transalate node path to angle/distance segments
segments = []
for u, v in zip(node_path, node_path[1:]):
    x1, y1 = MAZE_JUNCTIONS[u]
    x2, y2 = MAZE_JUNCTIONS[v]
    dx = x2 - x1
    dy = y2 - y1
    # Calculate the arctangent of y/x
    angle = math.atan2(-dy, dx)
    # Calculate the hypotenuse of the right triangle
    dist = math.hypot(dx, dy)
    segments.append((angle, dist))

# Calibrated constants
"""Measure values:

1) Mark a 50 cm line on the floor.
2) Run both servos and measure how long it takes to cross the mark.
3) For rotation: point the bot in a corner, spin one wheel forward and 
   one backward at throttle=0.5, measure how long it takes to rotate 90 degree.

LINEAR_SPEED = measured distance cm / measured time in seconds
ANGULAR_SPEED = math.radians(90) / measured time in seconds
"""
LINEAR_SPEED = 20.0 # cm/s at throttle=1.0  
ANGULAR_SPEED = math.pi/2 # rad/s at throttle=1.0

# Set up HAT and bot
kit = ServoKit(channels=16)
left_s = kit.continuous_servo[0]
right_s = kit.continuous_servo[1]

def spin(throttle_left, throttle_right, duration_s):
    left_s.throttle = throttle_left
    right_s.throttle = throttle_right
    time.sleep(duration_s)
    left_s.throttle = 0
    right_s.throttle = 0

# Execute each segment (angle, dist)
for angle, dist in segments:
    # Turn in place, the angle is in between pi and -pi.
    # Explain delta calculation: 
    ## (target - current) is the raw difference (could be -inf to inf).
    ## + pi % 2pi wraps the result in the inteval 0 to 2pi.
    ## -pi shifts it to end up in the range -pi to pi.
    delta = ((angle - current_theta + math.pi) % (2*math.pi)) - math.pi
    t = abs(delta) / ANGULAR_SPEED
    direction = math.copysign(1, delta) # 1 if delta>0, -1 if delta<0
    spin(left_s=direction,
         right_s=-direction, # opposite direction
         duration_s=t)
    current_theta = angle

    # Drive straight
    t = dist / LINEAR_SPEED
    spin(1,1,t)
