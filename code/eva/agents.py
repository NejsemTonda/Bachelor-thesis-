import random
from Box2D.b2 import vec2
from enum import Enum
import numpy as np
from eva.helpers import get_possible_points



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

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def new(level, node_count=20):
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
            edges.append((n, n2, random.choice([Type.plank, Type.road])))
        
        for _ in range(node_count*2):
            n1 = random.choice(nodes)
            n2 = random.choice(nodes)
            l = (vec2(n1.pos) - vec2(n2.pos)).length 
            if n1 in n2.edges or n1 == n2 or l > level.env.max_plank_len or l < 0.1:
                continue
            n1.edges.append(n2)
            n2.edges.append(n1)
            edges.append((n1, n2, random.choice([Type.plank, Type.road])))
        
        return GraphGenome(nodes, edges) 

    def better_init(level, alpha=1):
        def make_line(nodes, edges, start_n, end_n, t):
            last = start_n
            direction = vec2(end_n.pos)-vec2(start_n.pos)
            direction = direction / direction.length
            while True:
                if (vec2(last.pos)-vec2(end_n.pos)).length < 1.5:
                    break
                l = random.randint(4, 8)/4
                new_pos = vec2(last.pos)+l*direction
                new_pos = vec2(list(map(int,vec2(new_pos)*4)))/4
                if (vec2(last.pos)-new_pos).length > 2.05:
                    continue
                new_node = GraphGenome.Node(tuple(new_pos))
                nodes.append(new_node)
                new_node.edges.append(last)
                last.edges.append(new_node)
                edges.append((last, new_node, t))
                last = new_node

            if (vec2(last.pos) - vec2(end_n.pos)).length > 0.1:
                last.edges.append(end_n)
                end_n.edges.append(last)
                edges.append((last, end_n, t))

        edges = []
        nodes = [GraphGenome.Node(pos) for pos in level.env.anchor_dic.keys()]
        level_anchors = len(nodes)
        left = nodes[level.left_side]
        right = nodes[level.right_side]
        fixed = list(filter(lambda x: x not in [left,right], nodes))
            
        # Create road
        make_line(nodes, edges, left, right, Type.road)

        # Create supporst from fixed anchors
        for node in fixed:
            target = random.choice(nodes[level_anchors:])
            make_line(nodes, edges, node, target, Type.plank)
        
        ## reinforce
        for n1, n2 in zip(nodes, nodes[1:]):
            possible = get_possible_points([n1.pos, n2.pos]) 
            if len(possible) == 0:
                continue
            new_node = GraphGenome.Node(random.choice(possible))
            for node in nodes:
                l = (vec2(node.pos)-vec2(new_node.pos)).length
                if l > 0.1 and l < level.env.max_plank_len and random.random() < alpha:
                    new_node.edges.append(node) 
                    node.edges.append(new_node) 
                    edges.append((node, new_node, Type.plank))
        return GraphGenome(nodes, edges)
                  

if __name__ == "__main__":
    #g = KnapsackGenome.new(10)

    GraphGenome.new(l)
