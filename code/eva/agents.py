import random
from Box2D.b2 import vec2
from enum import Enum
import numpy as np



class Type(Enum):
    none = 0
    plank = 1
    road = 2

class Agent:
    def __init__(self, genome):
        self.fitness = None
        self.genome = genome

    def __repr__(self):
        return f"fitness: {self.fitness} from genome: {self.genome}"

    def __gt__(self, other):
        return self.fitness > other.fitness

class KnapsackGenome(list):
    def new(k_len):
        l = ["1" if random.random() < 0.5 else "0" for _ in range(k_len)]
        return KnapsackGenome(l)

    def __repr__(self):
        return "".join(self)

class SimpleGenome:
    def __init__(self, clicks, types):
        assert len(clicks) == len(types), f"lengths of clicks and types are mismatched {len(clicks)} {len(types)}"
        self.clicks = clicks
        self.types = types

    def new(level, length=20):
        clicks = [(
            random.randint(level.x_bounds[0]*4, level.x_bounds[1]*4)/4,
            random.randint(level.y_bounds[0]*4, level.y_bounds[1]*4)/4,
            ) for _ in range(length)
        ]
        types = random.choices([Type.plank, Type.road, Type.none], k=length)
        return SimpleGenome(clicks, types)

    def __repr__(self):
        return f"clicks = {self.clicks}, types = {self.types}"

class PolarGenome:
    def __init__(self, clicks, types):
        assert len(clicks) == len(types), f"lengths of clicks and types are mismatched {len(clicks)} {len(types)}"
        self.clicks = clicks
        self.types = types

    def new(level, length=20):
        clicks = [(level.env.max_plank_len*random.random(), random.random()*np.pi*2) for _ in range(length)]
        types = random.choices([Type.plank, Type.road, Type.none], k=length, weights=[1,1,0])
        return SimpleGenome(clicks, types)

    def __repr__(self):
        return f"clicks = {self.clicks}, types = {self.types}"


class GraphGenome:
    class Node:
        def __init__(self, pos):
            self.pos = pos
            self.edges = []

    class Edge:
        def __init__(self, v1, v2, t):
            self.nodes = [v1,v2]
            self.type = t

        def __getitem__(self, key):
            return self.nodes[key] 

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def new(level, node_count=20, edge_count=20):
        nodes = [GraphGenome.Node(pos) for pos in level.env.anchor_dic.keys()]
        edges = []
        while len(nodes) < node_count:
            n = random.choice(nodes)
            target = (
                random.randint(level.x_bounds[0]*4, level.x_bounds[1]*4)/4,
                random.randint(level.y_bounds[0]*4, level.y_bounds[1]*4)/4,
            ) 
            l = (vec2(target)-vec2(n.pos)).length
            if l > level.env.max_plank_len or l < 0.25:
                continue

            for n2 in n.edges:
                if target == n2.pos:
                    break
            else:
                n2 = GraphGenome.Node(target)

            nodes.append(n2)
            n.edges.append(n2)
            n2.edges.append(n)
            edges.append(GraphGenome.Edge(n, n2, random.choice([Type.plank, Type.road, Type.none])))
        
        for _ in range(node_count*2):
            n1 = random.choice(nodes)
            n2 = random.choice(nodes)
            l = (vec2(n1.pos) - vec2(n2.pos)).length 
            if n1 in n2.edges or n1 == n2 or l > level.env.max_plank_len or l < 0.1:
                continue
            n1.edges.append(n2)
            n2.edges.append(n1)
            edges.append(GraphGenome.Edge(n1, n2, random.choice([Type.plank, Type.road, Type.none])))

        return GraphGenome(nodes, edges) 
                
          

if __name__ == "__main__":
    #g = KnapsackGenome.new(10)

    GraphGenome.new(l)
