import time 
from collections import deque
from .heading_utils import heading_lookup

HEADINGS = ["N", "E", "S", "W"]

def main_loop(wb, tape_follower, maze, read_id,
              target_id=5, dfs_timeout=1.0):
    """
    Arguments:
    - wb: Wheelbase object (drive/stop)
    - tape_follower: TapeFollower instance (step() -> bool)
    - maze: Maze Graph 
    - read_id: callable -> int 
    - target_id: goal tag
    - dfs_timout: second to wait at junction before assuming dead-end
    """
    phase = 1
    stack = deque()
    current = last_tag = None
    current_heading = "N"
    last_junction_t = time.time()

    while True:
        if tape_follower.step():
            wb.stop()
            last_junction_t = time.time()
            id_seen = None
            while id_seen is None and time.time() - last_junction_t < dfs_timeout:
                id_seen = read_id()
                yield # allow pygame to refresh
            
            if id_seen is None:
                # Treat as a dead-end and U-turn
                wb.drive(0.5, -0.5, 1.1); yield
                continue
            
            # Update the graph
            last_tag, current = current, id_seen
            if last_tag is not None:
                maze.add_edge_visit(last_tag, current, weight=time.time())
            
            # Phase logic
            if phase == 1:
                unexpl = maze.unexplored_neighbors(current)
                if unexpl:
                    stack.append(current)
                    next_tag = unexpl[0]
                elif stack:
                    next_tag = stack.pop()
                else:
                    phase = 2
                    continue # re-enter loop to BFS

                turn_cmd = _turn_to(current, next_tag, current_heading, wb)
                current_heading = turn_cmd
                yield
            
            if phase == 2:
                opt_path = maze.shortest(current, target_id)
                path_i = 0
                phase = 3
                continue
            
            if phase == 3:
                if current == target_id:
                    wb.stop()
                    print("Goal reached")
                    return
                path_i += 1
                next_tag = opt_path[path_i]
                turn_cmd = _turn_to(current, next_tag, current_heading, wb)
                current_heading = turn_cmd
                yield 
        yield # Keep loop cooperative

# Turning function
def _turn_to(frm, to, curr_heading, wb,
             arc_speed=0.5,
             inner_speed=0.0,
             arc_time=0.25,
             straighten_speed=0.35,
             straighten_time=0.06,
             mute_buffer=0.1):           
    desired = heading_lookup(frm, to)
    diff = (HEADINGS.index(desired) - HEADINGS.index(curr_heading)) % 4
    
    if diff == 1: # right
        wb.drive(arc_speed, inner_speed, arc_time)
    elif diff == 3: # left
        wb.drive(inner_speed, arc_speed, arc_time)
    elif diff == 2:
        wb.drive(arc_speed, inner_speed, arc_time)
        wb.drive(inner_speed, arc_speed, arc_time)
    
    # Small forward nudge
    wb.drive(straighten_speed, straighten_speed, straighten_time)
    # Set a minimum time before the next junction can fire
    total_move = arc_time * (2 if diff==2 else 1) + straighten_time
    wb.ignore_junction_until = time.time() + total_move + mute_buffer
    return desired


