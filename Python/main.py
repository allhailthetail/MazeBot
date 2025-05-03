"""
PHASE 1  DFS until graph is complete
PHASE 2  run BFS once on the finished graph
PHASE 3  drive the optimal route to the goal
"""

from motor_driver import WheelBase
from tag_reader import read_id
from graph_builder import MazeGraph
from line_follow import TapeFollower 
from heading_utils import heading_lookup
import time
from collections import deque

# Configuration
TARGET_ID = 5
START_ID = 5
stack = [] # DFS backtract stack
HEADINGS = ["N", "E", "S", "W"]
heading_at = {}
current_heading = "N"


# Hardware components
wb = WheelBase()
maze = MazeGraph()
tf = TapeFollower(wb)

# Define function to turn
def turn_command(frm, to):
    global current_heading
    desired_heading = heading_lookup(frm, to)
    diff = (HEADINGS.index(desired_heading) -
            HEADINGS.index(current_heading)) % 4
    
    if diff == 1: # right
        wb.drive(0.5, -0.5, 0.55)
    elif diff == 3: # left
        wb.drive(-0.5, 0.5, 0.55)
    elif diff == 2: # U turn
        wb.drive(0.5, -0.5, 1.1)
    current_heading = desired_heading
    wb.drive(0.35, 0.35, 0.12)

phase = 1
curr = None

def choose_dfs_neighbor(node):
    """Unexplored neighbor if any, else pop stack"""
    u = maze.unexplored_neighbors(node)
    if u:
        stack.append(node)
        return u[0] # first unexplored edge
    elif stack:
        return stack.pop() # backtrack
    else:
        return None

while True:
    # FOLLOW_EDGE block
    if tf.step():
        wb.stop()
        time.sleep(0.1)
        tag = read_id()
        if tag is None:
            continue # try again

        prev = curr
        curr = tag
        if START_ID is None: 
            START_ID = curr

        # Store the edge just traversed (prev -> curr)
        if prev is not None:
            maze.add_edge_visit(prev, curr,
                                weight=time.time())
        
        # Phases logic
        if phase == 1:
            nxt = choose_dfs_neighbor(curr)
            if nxt is None:
                print("DFS finished, switching to BFS")
                phase = 2
                continue
            turn_command(curr, nxt)
        elif phase == 2:
            optimal = maze.shortest(curr, TARGET_ID)
            print("Optimal path:", optimal)
            phase = 3
            path_index = 0
            continue
        elif phase == 3:
            path_index += 1
            if path_index >= len(optimal):
                print("Goal Reached")
                wb.stop()
                break
            nxt = optimal[path_index]
            turn_command(curr, nxt)
