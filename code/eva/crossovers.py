import random
from eva.agents import Agent, SimpleGenome, KnapsackGenome


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
        parent1 = agents[i].genome
        parent2 = agents[i*2+1].genome

        points = [random.randint(0, len(agents[0].genome.types)) for _ in range(n)]

        child1_clicks, child2_clicks = vector_cx(parent1.clicks, parent2.clicks, points) 
        child1_types, child2_types = vector_cx(parent1.types, parent2.types, points)

        offspring.append(Agent(SimpleGenome(child1_clicks, child1_types)))
        offspring.append(Agent(SimpleGenome(child2_clicks, child2_types)))
    return offspring

def graph_cx(agents):
    return agents

if __name__ == "__main__":
    a = [1,2,3,4,5]
    b = ['a', 'b', 'c', 'd', 'e']
    print(vector_cx(a, b, points=2))
    print(vector_cx(a, b, points=[2]))
    print(vector_cx(a, b, points=[2,4]))
    print(vector_cx(a, b, points=[1,2,4]))
