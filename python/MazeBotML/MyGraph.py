import numpy as np
import math
from pprint import pformat
import heapq

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


class MyGraph():
    def __init__(self):
        # Adjency matrix
        self.adj = {}
    
    def add_edge(self, u, v, weight=1):
        if weight is None:
            weight = 1

        # Add nodes if not in the graph 
        if u not in self.adj:
            self.adj[u] = {}
        if v not in self.adj:
            self.adj[v] = {}
        
        # Add edge between them (undirected)
        self.adj[u][v] = weight
        self.adj[v][u] = weight
    
    def shortest_path(self, start, target):
        # Initialize the shortest path dictionary
        shortest_paths = {vertex: float("inf") for vertex in self.adj}
        shortest_paths[start] = 0

        # Keep track of predecessors (useful to find shortest path)
        predecessors = {vertex: None for vertex in self.adj}

        # Priority queue stores current distance and vertex
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            # Skip if greater the shortest path already present
            if current_distance > shortest_paths[current_vertex]:
                continue
            
            # Iterate through neighbors of the current vertex
            for neighbor, attr in self.adj[current_vertex].items():
                # Ensure numerical values for the weights
                weight = attr if isinstance(attr, (int, float)) else attr["weight"]
                distance = current_distance + weight

                # Update shortest path if needed
                if distance < shortest_paths[neighbor]:
                    shortest_paths[neighbor] = distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        # Reconstruct the shortest path
        shortest_path = []
        while target:
            shortest_path.append(target)
            target = predecessors[target]
        
        # Target not reacheable
        if not shortest_path or shortest_path[-1] != start:
            return []
        
        return shortest_path[::-1] 
    
    def path_length(self, path):
        total = 0.0
        for u, v in zip(path, path[1:]):
            weight = self.adj[u][v]
            total += weight

        return total


    def __str__(self):
        return pformat(self.adj, indent=2, width=80)


if __name__ == "__main__":
    G = MyGraph()
    for u, v in MAZE_EDGES:
        x1, y1 = MAZE_JUNCTIONS[u]
        x2, y2 = MAZE_JUNCTIONS[v]
        dist = math.hypot(x2 - x1, y2 - y1)
        G.add_edge(u, v, weight=dist)
    print(G)
        
    

        

        