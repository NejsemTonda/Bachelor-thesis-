import eva.crossovers as cx
import eva.mutations as mut
import eva.fitness as fits
import eva.selections as sel
import eva.agents as agents
from eva.agents import Agent, Type
from eva.population import Population
from levels import LevelFactory
from functools import partial
from sim.ui import UI
from eva.fitness import graph_fitness

from Box2D.b2 import vec2

import random
import numpy as np

import pickle

l = [
'best-lvl1-2024-05-06 15:37:48.147057',
'best-lvl1-2024-05-06 18:14:59.476695',
'best-lvl1-2024-05-07 09:17:13.033081',
'best-lvl1-2024-05-07 10:38:50.909697',
'best-lvl1-2024-05-07 12:04:57.179887',
'best-lvl1-2024-05-07 13:30:04.446417',
'best-lvl2-2024-05-06 16:14:55.298528',
'best-lvl2-2024-05-06 18:51:09.963916',
'best-lvl2-2024-05-07 09:36:22.223799',
'best-lvl2-2024-05-07 10:56:57.553656',
'best-lvl2-2024-05-07 12:27:04.105605',
'best-lvl2-2024-05-07 13:51:22.356596',
'best-lvl3-2024-05-06 17:01:50.619338',
'best-lvl3-2024-05-07 10:01:47.214088',
'best-lvl3-2024-05-07 11:21:30.080132',
'best-lvl3-2024-05-07 12:53:24.370713',
'best-lvl3-2024-05-07 14:19:45.744006',
'best-lvl4-2024-05-06 17:38:05.530984',
'best-lvl4-2024-05-07 10:19:39.603988',
'best-lvl4-2024-05-07 11:43:34.941671',
'best-lvl4-2024-05-07 13:08:44.441096',
'best-lvl4-2024-05-07 14:38:43.646257',
]

name = l[-2]
with open(name, 'rb') as file:
    agent = pickle.load(file)

level = LevelFactory.level4()
for e in agent.genome.edges:
    if e[2] == Type.plank:
        print(vec2(e[0].pos), vec2(e[1].pos), e[2])
        level.env.add_plank(vec2(e[0].pos), vec2(e[1].pos))

    elif e[2] == Type.road:
        print(vec2(e[0].pos), vec2(e[1].pos), e[2])
        level.env.add_road(vec2(e[0].pos), vec2(e[1].pos))
    else:
        pass

level.env.init_graphics()
ui = UI(level.env)

while True:
    #level.env.step()
    level.env.draw()
    ui.update(level.env.world)
    print(ui.mouse_pos)
