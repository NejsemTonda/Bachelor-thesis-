from eva.agents import Type
import random

def simple(agents, click_p=0.1, click_max=1, type_p=0.05, type_weigths=[1,1,1]):
    types = [Type.plank, Type.road, Type.none]
    for a in agents:
        for i in range(len(a.genome.types)):
            if random.random() < type_p:
                a.genome.types[i] = random.choices(types, type_weigths)[0]
            if random.random() < click_p:
                c = a.genome.clicks[i]
                a.genome.clicks[i] = (c[0]+random.randint(-click_max,click_max), c[1]+random.randint(-click_max,click_max))

        if random.random() < click_p:
                c = a.genome.clicks[-1]
                a.genome.clicks[-1] = (c[0]+random.randint(-click_max,click_max), c[1]+random.randint(-click_max,click_max))

    return agents
