import pygame, math, networkx as nx
from env_and_robot import MAZE_EDGES, MAZE_JUNCTIONS, Envir, Robot
from Python.MyGraph import MyGraph

# Keep sprite in sync with pose
def refresh_sprite(r):
    r.rotated = pygame.transform.rotozoom(
        r.img, -math.degrees(r.theta), 1
    )
    r.rect = r.rotated.get_rect(center=(r.x, r.y))

# Configure nodes based on the maze
start_node = 6
goal_node = 19

# Build the graph and compute shortest path
G_1 = nx.Graph()
G = MyGraph()
# Add weights (euclidean distances)
for u, v in MAZE_EDGES:
    x1, y1 = MAZE_JUNCTIONS[u]
    x2, y2 = MAZE_JUNCTIONS[v]
    dist = math.hypot(x2 - x1, y2 - y1)
    G.add_edge(u, v, weight=dist)
    G_1.add_edge(u, v, weight=dist)

node_path = G.shortest_path(start=start_node, target=goal_node) # The output is something of the form [1, 2, 5]
path_length_mine = G.path_length(node_path)
node_path_nx = nx.shortest_path(G_1, start_node, goal_node, weight="weight") # weight = "weight"
path_length_nx = G.path_length(node_path_nx)

print(f"My shortest path: {node_path}, length: {path_length_mine}")
print(f"Nx shortest path: {node_path_nx}, length: {path_length_nx}")

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

# Setup for the pygame simulation
pygame.init()
clock = pygame.time.Clock()

environment = Envir((600, 1200))
robot = Robot(
    startpos=MAZE_JUNCTIONS[start_node],
    robotImg=r"C:\Users\Utente\OneDrive\Desktop\Maze_Bot\Bot Images\sampleBot.png",
    width=0.01*3779.52
)

segment_i = 0
phase = "turn"
x_goal, y_goal = None, None

# Main loop: turn -> drive -> next
running = True
while running:
    # Draw the maze
    environment.map.fill(environment.white)
    environment.draw_maze()

    # Quit if event triggered
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fixed time-rate
    dt = clock.tick(60) / 1000 # seconds elapsed
    #robot.move(dt)

    # Follow the segments until done
    if segment_i < len(segments):
        target_ang, remaining = segments[segment_i]

        if phase == "turn":
            # Compute the delta from the target angle
            delta = (target_ang - robot.theta + math.pi) % (2*math.pi) - math.pi
            turn_rate = 2.0 # rad/s
            step = turn_rate * dt
            if abs(delta) <=  step: # step
                robot.vl = robot.vr = 0
                robot.theta = target_ang
                phase = "drive"
                # Lock in exact goal coords once
                _, next_node = node_path[segment_i], node_path[segment_i+1]
                x_goal, y_goal = MAZE_JUNCTIONS[next_node]
            else:
                robot.theta += step * (1 if delta > 0 else -1)

        elif phase == "drive":
            speed = 200 # pixels/s
            move = speed * dt
            dist_left = math.hypot(x_goal - robot.x, y_goal - robot.y)
            if move >= dist_left:
                robot.x, robot.y = x_goal, y_goal
                segment_i += 1
                phase = "turn"
            else:
                robot.x += math.cos(robot.theta) * move
                robot.y -= math.sin(robot.theta) * move
    

    print(f"{segment_i=} {phase=} x={robot.x:.1f} y={robot.y:.1f} "
      f"θ={math.degrees(robot.theta):.1f}")
    
    # Keep sprite up to date before drawing
    refresh_sprite(robot)
    
    # Draw robot overlays
    #environment.write_info(0, 0, robot.theta)
    robot.draw(environment.map)
    pygame.display.update()

pygame.quit()
