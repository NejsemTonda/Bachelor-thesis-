from eva.agents import Type
from Box2D.b2 import vec2
import numpy as np
from eva.helpers import pol2cart

SCALER = 4
def knapsack_fit(agent, knapsack):
    items = knapsack[0]
    max_w = knapsack[1]

    current_w = 0
    current_val = 0

    for g, item in zip(agent.genome, items):
        if g == "1":
            current_w += item['weight']
            current_val += item['value']
        if current_w > max_w:
            return 0

    return current_val


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
    min_d = round(min_d, ndigits=1)
    return min_d

def simple_fitness(agent, level, draw=False):
    level = level()
    clicks = map(vec2, agent.genome.clicks)
    last_click = vec2(list(level.env.anchor_dic.keys())[0])
    for c,t in zip(clicks, agent.genome.types):
        try:
            if t == Type.none:
                last_click = c
            elif t == Type.plank:
                added = level.env.add_plank(last_click, c)
                last_click = added.end/SCALER
                
            elif t == Type.road:
                added = level.env.add_road(last_click, c)
                last_click = added.end/SCALER
        except AssertionError:
            pass

    min_d = simulate(level, draw)
    fitness = -min_d

    return fitness

def polar_fitness(agent, level, draw=False):
    level = level()
    clicks = map(lambda x: vec2(pol2cart(x[0], x[1])), agent.genome.clicks) 
    last_click = vec2(list(level.env.anchor_dic.keys())[0])
    for c,t in zip(clicks, agent.genome.types):
        try:
            if t == Type.none:
                last_click += c
            elif t == Type.plank:
                added = level.env.add_plank(last_click, last_click+c)
                last_click = added.end/SCALER
                
            elif t == Type.road:
                added = level.env.add_road(last_click, last_click+c)
                last_click = added.end/SCALER
        except AssertionError:
            pass

    min_d = simulate(level, draw)
    fitness = -min_d

    return fitness

def improved_fitness(agent, level, alpha=0.1, beta=0.01, draw=False):
    level = level()
    fixed_anchors = list(level.env.anchor_dic.keys())[1:]
    fixed_a_cum_dist = 0
    clicks = map(lambda x: vec2(pol2cart(x[0], x[1])), agent.genome.clicks) 
    last_click = vec2(list(level.env.anchor_dic.keys())[0])
    for c,t in zip(clicks, agent.genome.types):
        try:
            if t == Type.none:
                last_click += c
            elif t == Type.plank:
                added = level.env.add_plank(last_click, last_click+c)
                last_click = added.end/SCALER
                for a in fixed_anchors:
                    if last_click == a:
                        fixed_anchors.remove(a)
                    else:
                        fixed_a_cum_dist += (vec2(a) - vec2(last_click)).length
            elif t == Type.road:
                added = level.env.add_road(last_click, last_click+c)
                last_click = added.end/SCALER
                for a in fixed_anchors:
                    if last_click == a:
                        fixed_anchors.remove(a)
                    else:
                        fixed_a_cum_dist+= (vec2(a) - vec2(last_click)).length

        except AssertionError:
            pass
    min_d = simulate(level, draw)

    new_anchor_discount = (len(level.env.anchor_dic) - len(fixed_anchors)) * (-alpha)
    fixed_a_discount = fixed_a_cum_dist * (-beta)

    fitness = -min_d + new_anchor_discount + fixed_a_discount
    return fitness 

def increasing_fitness(agent, level, hardness=0, draw=False):
    level = level()
    e = vec2(0,0.05)
    if hardness > 0:
        left = vec2(list(level.env.anchor_dic.keys())[0])
        right = vec2(list(level.env.anchor_dic.keys())[2])
        to = right + (left-right)*hardness
        to = vec2(list(map(int, to*4)))/4
        level.env.add_ground([right+e, to+e],anchors=[to])

    clicks = map(lambda x: vec2(pol2cart(x[0], x[1])), agent.genome.clicks) 
    last_click = vec2(list(level.env.anchor_dic.keys())[0])
    for c,t in zip(clicks, agent.genome.types):
        try:
            if t == Type.none:
                last_click += c
            elif t == Type.plank:
                added = level.env.add_plank(last_click, last_click+c)
                last_click = added.end/SCALER
                
            elif t == Type.road:
                added = level.env.add_road(last_click, last_click+c)
                last_click = added.end/SCALER
        except AssertionError:
            pass

    min_d = simulate(level, draw)
    fitness = -min_d

    return fitness

def graph_fitness(agent, level, draw=False):
    level = level()
    for e in agent.genome.edges:
        if e[2] == Type.plank:
            level.env.add_plank(vec2(e[0].pos), vec2(e[1].pos))

        elif e[2] == Type.road:
            level.env.add_road(vec2(e[0].pos), vec2(e[1].pos))
        else:
            pass

    min_d = simulate(level, draw)
    fitness = (-min_d, -level.env.cost)
    return fitness


def graph_increasing(agent, level, hardness=0, draw=False):
    level = level()
    e = vec2(0,0.05)
    if hardness > 0:
        left = vec2(list(level.env.anchor_dic.keys())[0])
        right = vec2(list(level.env.anchor_dic.keys())[2])
        to = right + (left-right)*hardness
        to = vec2(list(map(int, to*4)))/4
        level.env.add_ground([right+e, to+e],anchors=[to])


    for e in agent.genome.edges:
        if e[2] == Type.plank:
            level.env.add_plank(vec2(e[0].pos), vec2(e[1].pos))

        elif e[2] == Type.road:
            level.env.add_road(vec2(e[0].pos), vec2(e[1].pos))
        else:
            pass

    min_d = simulate(level, draw)
    fitness = -min_d
    return fitness


