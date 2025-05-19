import pygame, math

MAZE_JUNCTIONS = {
    1:  (100, 100),   2: (300, 100),   3: (500, 100),   4: (700, 100),
    5:  (900, 100),   6: (1100, 100),  7: (1100, 200),  8: (1100, 300),
    9:  (1100, 400), 10: (1100, 500), 11: (900, 500),  12: (700, 500),
    13: (500, 500),  14: (300, 500),  15: (100, 500),  16: (100, 400),
    17: (100, 300),  18: (100, 200),  19: (300, 300),  20: (500, 300),
    21: (700, 300),  22: (900, 300),  23: (300, 200),  24: (500, 200),
    25: (700, 200),  26: (900, 200),  27: (500, 400),  28: (700, 400),
    29: (300, 400),  30: (900, 400),
}

MAZE_EDGES = [
    # Outer perimeter (counter-clockwise)
    (1,2),(2,3),(3,4),(4,5),(5,6),
    (6,7),(7,8),(8,9),(9,10),(10,11),
    (11,12),(12,13),(13,14),(14,15),(15,16),
    (16,17),(17,18),(18,1),

    # Four vertical spines
    (2,23),(23,19),(19,29),(29,14),           # x = 300 px
    (3,24),(24,20),(20,27),(27,13),           # x = 500 px
    (4,25),(25,21),(21,28),(28,12),           # x = 700 px
    (5,26),(26,22),(22,30),(30,11),           # x = 900 px

    # Three horizontal corridors
    (23,24),(24,25),(25,26),                  # y = 200 px
    (19,20),(20,21),(21,22),                  # y = 300 px
    (29,27),(27,28),(28,30),                  # y = 400 px

    # A few inner diagonals for extra shortcuts
    (19,24),(20,25),(21,26),
    (29,28),(27,30)
]

# Create the environment 
class Envir:
    def __init__(self, dimensions): 
        # Colors 
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)
        # map dims
        self.height = dimensions[0]
        self.width = dimensions[1]
        # Window settings
        pygame.display.set_caption("Differential drive robot")
        self.map = pygame.display.set_mode((self.width,
                                            self.height))
        self.font = pygame.font.Font("freesansbold.ttf", 50)
        self.text = self.font.render("defaul", True, self.white, self.black)
        self.textRect = self.text.get_rect()
        self.textRect.center = (dimensions[1]-650,
                                dimensions[0]-100)
        # Trail
        self.trail_set = []

    def write_info(self, Vl, Vr, theta):
        txt = f"VL = {Vl} VR = {Vr}  Theta = {int(math.degrees(theta))}"
        self.text = self.font.render(txt, True, self.white, self.black)
        self.map.blit(self.text, self.textRect)
    
    def trail(self, pos):
        for i in range(0, len(self.trail_set)-1):
            pygame.draw.line(self.map,
                             self.yel,
                             (self.trail_set[i][0], self.trail_set[i][1]),
                             (self.trail_set[i+1][0], self.trail_set[i+1][1]))
        if self.trail_set.__sizeof__() > 30000:
            self.trail_set.pop(0)
        self.trail_set.append(pos)
    
    def robot_frame(self, pos, rotation):
        n = 80
        centerx, centery = pos
        x_axis = (centerx + n*math.cos(-rotation), centery + n*math.sin(-rotation))
        y_axis = (centerx + n*math.cos(-rotation+math.pi/2), 
                  centery + n*math.sin(-rotation+math.pi/2))
        pygame.draw.line(self.map, self.red, (centerx, centery), x_axis, 3)
        pygame.draw.line(self.map, self.green, (centerx, centery), y_axis, 3)

    def draw_tape_segment(self, start, end, width, color):
        # Build a rectangle of thickness= width along start to end
        x1, y1 = start
        x2, y2 = end
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        ux, uy = dx/length, dy/length # unit vector along segment
        px, py = -uy, ux # perp unit vector
        hw = width/2
        corners = [
            (x1 + px*hw, y1 + py*hw),
            (x1 - px*hw, y1 - py*hw),
            (x2 - px*hw, y2 - py*hw),
            (x2 + px*hw, y2 + py*hw),
        ]
        pygame.draw.polygon(self.map, color, corners)

    def draw_maze(self):
        tape_w = 30
        
        # Draw each edge as a thick black line
        for u,v in MAZE_EDGES:
            self.draw_tape_segment(MAZE_JUNCTIONS[u],
                                   MAZE_JUNCTIONS[v],
                                   tape_w, self.black)
            
        for cx, cy in MAZE_JUNCTIONS.values():
            # radius = half your tape width 
            pygame.draw.circle(self.map, self.black, (cx, cy), tape_w//2 + 1)
        
        # Draw AprilTag "rectangles" + labels
        self.tags = {}
        for tid, (cx, cy) in MAZE_JUNCTIONS.items():
            rect = pygame.Rect(
                cx - tape_w/2,
                cy - tape_w/2,
                tape_w,
                tape_w
            )
            self.tags[tid] = rect
            pygame.draw.rect(self.map, self.red, rect, 1)
            self.tags[tid] = rect
            txt = self.font.render(str(tid), True, self.red)
            self.map.blit(txt, rect.move(-tape_w/2, -tape_w))

    
    def draw_sensors(self, robot, surface):
        # Draw a 4px dot at each sensor location
        for idx, (offx, offy) in enumerate(robot.sensor_offset):
            dx = offx*math.cos(robot.theta) - offy*math.sin(robot.theta)
            dy = -offx*math.sin(robot.theta) - offy*math.cos(robot.theta)
            px = int(robot.x + dx)
            py = int(robot.y + dy)
            col = self.green if idx == 0 else self.red
            pygame.draw.circle(surface, col, (px, py), 4)

class Robot:
    def __init__(self, startpos, robotImg, width):
        self.m2p = 3779.52 # Convert m/s to pixels/s
        # Robot dimensions
        self.w = width
        self.x = startpos[0]
        self.y = startpos[1]
        self.theta = 0
        self.vl = 0.03 * self.m2p 
        self.vr = 0.03 * self.m2p
        self.maxspeed = 0.05 * self.m2p
        self.minspeed = -0.05 * self.m2p
        # Graphics
        self.img = pygame.image.load(robotImg)
        self.rotated = self.img 
        self.rect = self.rotated.get_rect(center=(self.x,
                                                  self.y))
        self.sensor_offset = [(40, -10), # Left sensor: 40px forward, 15px right
                              (40, 10)] # right sensor
    
    def draw(self, map):
        map.blit(self.rotated, self.rect)
    
    def move(self, dt, event=None):

        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP4:
                    self.vl += 0.001 * self.m2p
                elif event.key == pygame.K_KP1:
                    self.vl -= 0.001 * self.m2p
                elif event.key == pygame.K_KP6:
                    self.vr += 0.001 * self.m2p
                elif event.key == pygame.K_KP3:
                    self.vr -= 0.001 * self.m2p

        self.x += ((self.vl + self.vr) / 2) * math.cos(self.theta) * dt
        self.y -= ((self.vl + self.vr) / 2) * math.sin(self.theta) * dt # Minus sign b/c the y-axis for the robot is in opposite direction compared to the screen
        self.theta += (self.vr-self.vl)/self.w * dt
        # Reset theta to stay between -2pi and 2pi
        if self.theta > 2*math.pi or self.theta < -2*math.pi:
            self.theta = 0
        # Set max speed
        self.vr = min(self.vr, self.maxspeed)
        self.vl = min(self.vl, self.maxspeed)
        # Set min speed
        self.vr = max(self.vr, self.minspeed)
        self.vl = max(self.vl, self.minspeed)

        self.rotated = pygame.transform.rotozoom(self.img,
                                        math.degrees(self.theta), 
                                        1)
        self.rect = self.rotated.get_rect(center=(self.x, self.y))
    
    def read_sensor(self, idx, surface):
        offx, offy = self.sensor_offset[idx]
        # Rotate offset by theta
        dx = offx*math.cos(self.theta) - offy*math.sin(self.theta)
        dy = -offx*math.sin(self.theta) - offy*math.cos(self.theta)
        px = int(self.x + dx)
        py = int(self.y + dy)
        print(f"SENSOR #{idx}: sample at ({px},{py}) = {surface.get_at((px,py))}")
        # Restrict to inside the window
        if 0 <= px < surface.get_width() and 0 <= py < surface.get_height():
            r, g, b, _ = surface.get_at((px, py))
            return 0 if (r,g,b) == (0, 0, 0) else 1 # .white
        return 1
