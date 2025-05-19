import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import networkx as nx
from env_and_robot import MAZE_JUNCTIONS, MAZE_EDGES, Envir, Robot
import time

class MazeGraph:
    def __init__(self):
        self.G = nx.Graph()
        # Add every possible edge
        self.G.add_edges_from(MAZE_EDGES) # full topology
        # assign default weight to 1
        for u, v in MAZE_EDGES:
            self.G[u][v]["weight"] = 1
        self.explored = set()
    
    def add_edge_visit(self, u, v, weight):
        self.G[u][v]["weight"] = weight
        self.explored.add(frozenset((u,v))) # Frozen set can't be changed
    
    def unexplored_neighbors(self, node):
        """Return list of neighbor IDs that have not been traversed yet"""
        return [nbr for nbr in self.G.neighbors(node)
                if frozenset((node, nbr)) not in self.explored]

    def is_complete(self):
        return all(not self.unexplored_neighbors(n) for n in self.G.nodes)
    
    def add_tag(self, tag_id):
        now = time.time()
        if self.last_tag is not None:
            dt = now - self.last_time # distance proxy
            self.G.add_edge(self.last_tag, tag_id, weight=dt)
        self.last_tag = tag_id
        self.last_time = now
    
    def shortest(self, start, goal):
        return nx.shortest_path(self.G, start, goal, weight="weight")
