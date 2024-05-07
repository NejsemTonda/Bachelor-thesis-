from eva.agents import Type, GraphGenome
import random
import numpy as np
from Box2D.b2 import vec2
from eva.helpers import get_possible_points
import copy

def knapsack(agents):
    for a in agents:
        for i in range(len(a.genome)):
            if random.random() < 1/len(a.genome):
                a.genome[i] = "1" if a.genome[i] == "0" else "0"
    return agents

def simple(agents, click_p=0.1, click_max=1, type_p=0.05, type_weigths=[1,1,1]):
    types = [Type.plank, Type.road, Type.none]
    for a in agents:
        for i in range(len(a.genome.types)):
            if random.random() < type_p:
                a.genome.types[i] = random.choices(types, type_weigths)[0]
            if random.random() < click_p:
                c = a.genome.clicks[i]
                a.genome.clicks[i] = (c[0]+random.randint(-click_max,click_max), c[1]+random.randint(-click_max,click_max))
    return agents


def polar(agents, click_p=0.1, angle_max=np.pi/12,len_max=0.5, type_p=0.05, type_weigths=[1,1,0]):
    types = [Type.plank, Type.road, Type.none]
    agents = copy.deepcopy(agents)
    for a in agents:
        for i in range(len(a.genome.types)):
            if random.random() < type_p:
                a.genome.types[i] = random.choices(types, type_weigths)[0]
            if random.random() < click_p:
                c = a.genome.clicks[i]
                a.genome.clicks[i] = (
                    max(0.25,c[0]+(2*random.random()-1)*len_max),
                    (c[1]+(2*random.random()-1)*angle_max) % (np.pi*2)
                )

    return agents

def graph(agents, node_p=1, type_p=1):
    for a in agents:
        if random.random() < node_p:
            for node in a.genome.nodes:
                if random.random() < 1/len(a.genome.nodes):
                    possible = get_possible_points([node.pos]+[n.pos for n in node.edges])
                    node.pos = random.choice(possible) if len(possible) > 0 else node.pos
        if random.random() < type_p:
            i = 0
            while i < len(a.genome.edges):
                e = a.genome.edges[i]
                if random.random() < 1/len(a.genome.edges):
                    x = random.random()
                    if x < 0.5:
                       a.genome.edges[i] = (e[0], e[1], Type.plank if e[2] == Type.road else Type.road)
                    elif x < 0.75 and len(a.genome.edges) < len(a.genome.nodes)*5:
                        for _ in range(20):
                            n1 = random.choice(a.genome.nodes)
                            n2 = random.choice(a.genome.nodes)
                            l = (vec2(n1.pos)-vec2(n2.pos)).length 
                            if n1 not in n2.edges or n2 not in n1.edges or l > 2.05 or l < 0.1:
                                continue
                            n1.edges.append(n2)
                            n2.edges.append(n1)
                            a.genome.edges.append((n1, n2, random.choice([Type.plank, Type.road])))
                            break
                    elif x < 1 and len(a.genome.edges) > len(a.genome.nodes):
                       e[0].edges.remove(e[1])
                       e[1].edges.remove(e[0])
                       a.genome.edges.remove(e)
                i += 1 
    return agents



