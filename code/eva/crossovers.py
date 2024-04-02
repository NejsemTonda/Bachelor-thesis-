import random
from eva.agents import Agent, SimpleGenome

def n_point(agents, n=1):
    assert n < len(agents[0].genome.types), "cannot perform {n}-point crossover on genome of len={len(agents[0].genome.types)}"
    assert n < 2, "not implemeted yet"
    offspring = []
    for i in range(len(agents)//2):
        parent1 = agents[i].genome
        parent2 = agents[i*2+1].genome

        point = random.randint(0, len(agents[0].genome.types))

        child1_clicks = parent1.clicks[:point]+parent2.clicks[point:]
        child1_types = parent1.types[:point]+parent2.types[point:]

        child2_clicks = parent2.clicks[:point]+parent1.clicks[point:]
        child2_types = parent2.types[:point]+parent1.types[point:]

        offspring.append(Agent(SimpleGenome(child1_clicks, child1_types)))
        offspring.append(Agent(SimpleGenome(child2_clicks, child2_types)))
    return offspring
