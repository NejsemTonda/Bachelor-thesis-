from eva.agents import Type
import random
import numpy as np

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


def radian(agents, click_p=0.1, angle_max=np.pi/12,len_max=0.5, type_p=0.05, type_weigths=[1,1,1]):
    types = [Type.plank, Type.road, Type.none]
    for a in agents:
        for i in range(len(a.genome.types)):
            if random.random() < type_p:
                a.genome.types[i] = random.choices(types, type_weigths)[0]
            if random.random() < click_p:
                c = a.genome.clicks[i]
                a.genome.clicks[i] = (c[1]+(2*random.randint-1)*len_max, c[0]+(2*random.random()-1)*angle_max)

    return agents


