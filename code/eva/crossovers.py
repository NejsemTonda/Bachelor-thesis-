import random
from eva.agents import Agent, SimpleGenome, KnapsackGenome, Type
import copy


def vector_cx(a, b, points=None):
    assert len(a) == len(b), f"length of a != length of b {len(a)} != {len(b)}"
    if points is None:
        return a,b
    if isinstance(points, int): points = [points]

    for p in points:
        assert p <= len(a) and p <= len(b), f"point {p} was outside of bound"
        
        a_t = a[:p] + b[p:]
        b_t = b[:p] + a[p:] 

        a,b = a_t, b_t 

    return a,b

def knapsack_cx(agents):
    offspring = []
    for i in range(len(agents)//2):
        parent1 = agents[i].genome
        parent2 = agents[i*2+1].genome

        point = random.randint(0, len(agents[0].genome))

        child1, child2 = vector_cx(parent1, parent2, point) 

        offspring.append(Agent(KnapsackGenome(child1)))
        offspring.append(Agent(KnapsackGenome(child2)))

    return offspring

def n_point(agents, n=1):
    assert n < len(agents[0].genome.types), "cannot perform {n}-point crossover on genome of len={len(agents[0].genome.types)}"
    assert n < 2, "not implemeted yet"
    offspring = []
    for i in range(len(agents)//2):
        parent1 = copy.deepcopy(agents[i].genome)
        parent2 = copy.deepcopy(agents[i*2+1].genome)

        points = [random.randint(0, len(agents[0].genome.types)) for _ in range(n)]

        child1_clicks, child2_clicks = vector_cx(parent1.clicks, parent2.clicks, points) 
        child1_types, child2_types = vector_cx(parent1.types, parent2.types, points)

        offspring.append(Agent(SimpleGenome(child1_clicks, child1_types)))
        offspring.append(Agent(SimpleGenome(child2_clicks, child2_types)))
    return offspring

def graph_cx(agents, phi=1):
    return agents
    def split(agent, x=None, y=None):
        set1 = []
        set2 = []
        assert x is not None and y is not None, "can only cross agent by one line"
            
        for node in agent.genome.nodes:
            if x is not None:
                if node.pos[0] > x:
                    set1.append(node)
                else:
                    set2.append(node)
            if y is not None:
                if node.pos[1] > y:
                    set1.append(node)
                else:
                    set2.append(node)
        for node in agent.genome.node:
            for e in node.edges:
                if node in set1 and e in set2 or node in set2 and e in set1:
                    node.genome.remove(e)
                    if (e, node, Type.road) in agents.genome.edges:
                        agents.genome.edges.remove((e, node, Type.road))
                    elif (node, e, Type.road) in agents.genome.edges:
                        agents.genome.edges.remove((node, e, Type.road))
                    elif (node, e, Type.plank) in agents.genome.edges:
                        agents.genome.edges.remove((node, e, Type.plank))
                    elif (e, node, Type.plank) in agents.genome.edges:
                        agents.genome.edges.remove((e, node, Type.plank))

        return set1, set2

    offspring = []
    for i in range(len(agents)//2):
        parent1 = copy.deepcopy(agents[i].genome)
        parent2 = copy.deepcopy(agents[i*2+1].genome)
        max_x = max([node.pos[0] for node in parent1.genome.nodes] + [node.pos[0] for node in parent2.genome.nodes])
        min_x = min([node.pos[0] for node in parent1.genome.nodes] + [node.pos[0] for node in parent2.genome.nodes])
        max_y = max([node.pos[1] for node in parent1.genome.nodes] + [node.pos[1] for node in parent2.genome.nodes])
        min_y = max([node.pos[1] for node in parent1.genome.nodes] + [node.pos[1] for node in parent2.genome.nodes])

        use_y = random.random() < 0.5
        point = random.randint(min_y if use_y else min_x, min_y if use_y else max_x) 

        p1_s1, p1_s2 = split(parent1, y=point) if use_y else split(parent1, x=point)
        p2_s1, p2_s2 = split(parent2, y=point) if use_y else split(parent2, x=point)

        child1 = GraphGenome(p1_s1+p2_s2, [])
        child2 = GraphGenome(p2_s1+p1_s2, [])

        offspring.append(child1)
        offspring.append(child2)

    return offspring






if __name__ == "__main__":
    a = [1,2,3,4,5]
    b = ['a', 'b', 'c', 'd', 'e']
    print(vector_cx(a, b, points=2))
    print(vector_cx(a, b, points=[2]))
    print(vector_cx(a, b, points=[2,4]))
    print(vector_cx(a, b, points=[1,2,4]))
