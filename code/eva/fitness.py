import copy 
from eva.agents import Type
from Box2D.b2 import vec2
import numpy as np


def simulate(level, draw=False):
    min_d = float('inf')
    static = 0
    for _ in range(1000):
        level.env.step()
        if draw:
            level.env.draw()
        
        car = level.car.chassis
        if car.position.y < -10:
            break
        if car.linearVelocity.length < 0.01:
            static += 1
            if static > 15:
                break
        else:
            static = 0

        min_d = min(min_d, (car.position - level.goal).length)

    return min_d

def simple_fitness(agent, level, draw=False):
    if agent.fitness is not None and not draw:
        return agent.fitness

    level = level()
    clicks = map(vec2, agent.genome.clicks)
    last_click = vec2(list(level.env.anchor_dic.keys())[0])
    for c,t in zip(clicks, agent.genome.types):
        try:
            if t == Type.none:
                last_click = c
            elif t == Type.plank:
                added = level.env.add_plank(last_click, c)
                last_click = added.end
                
            elif t == Type.road:
                added = level.env.add_road(last_click, c)
                last_click = added.end
        except AssertionError:
            pass

    min_d = simulate(level, draw)
    fitness = -min_d

    return fitness

def fitness_radians(aget, level, draw=False)
    def pol2cart(l, alpha):
        x = l * np.cos(alpha)
        y = l * np.sin(alpha)
        return(x, y)

    if agent.fitness is not None and not draw:
        return agent.fitness

    level = level()
    clicks = map(vec2, agent.genome.clicks)
    last_click = vec2(list(level.env.anchor_dic.keys())[0])
    for c,t in zip(clicks, agent.genome.types):
        c = pol2cart(c)
        try:
            if t == Type.none:
                last_click = c
            elif t == Type.plank:
                added = level.env.add_plank(last_click, c)
                last_click = added.end
                
            elif t == Type.road:
                added = level.env.add_road(last_click, c)
                last_click = added.end
        except AssertionError:
            pass

    min_d = simulate(level, draw)
    fitness = -min_d

    return fitness


