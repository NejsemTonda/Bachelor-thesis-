import sys
from sim.environment import Environment
from sim.ui import UI
from Box2D.b2 import vec2
from Box2D import b2Vec2
from levels import LevelFactory
import random 

import numpy as np



#lvl = LevelFactory.level1()
#env = lvl.env
#car = lvl.car
#env.add_road(vec2(6,5), vec2(8,5))
#env.add_road(vec2(8,5), vec2(10,5))
#env.add_road(vec2(10,5), vec2(12,5))
#env.add_road(vec2(12,5), vec2(19,5))
#
#env.add_plank(vec2(6,3),  vec2(7,4))
#env.add_plank(vec2(7,4),  vec2(8,5))
#env.add_plank(vec2(7,4),  vec2(6,5))
#env.add_plank(vec2(14,3),  vec2(13,4))
#env.add_plank(vec2(13,4),  vec2(12,5))
#env.add_plank(vec2(13,4),  vec2(14,5))
#env.add_plank(vec2(12,5), vec2(10,6.5))
#env.add_plank(vec2(10,5), vec2(10.5,6))
#env.add_plank(vec2(10,5), vec2(9.5,6))
#env.add_plank(vec2(9.5,6), vec2(8,5))
#env.add_plank(vec2(9.5,6), vec2(10.5,6))

lvl = LevelFactory.test()
env = lvl.env
car = lvl.car

env.add_road(b2Vec2(6,5), b2Vec2(10.25,5))
env.add_road(b2Vec2(8,5), b2Vec2(12,4.75))
env.add_road(b2Vec2(10,5), b2Vec2(13,5.25))
env.add_road(b2Vec2(12,5), b2Vec2(14,5))
env.add_plank(b2Vec2(6,5), b2Vec2(7.25,6.25))
env.add_plank(b2Vec2(7.25,6.25), b2Vec2(8,5))
env.add_plank(b2Vec2(8,5), b2Vec2(9,6.25))
env.add_plank(b2Vec2(9,6.25), b2Vec2(10,5))
env.add_plank(b2Vec2(10,5), b2Vec2(11,6.25))
env.add_plank(b2Vec2(11,6.25), b2Vec2(12,5))
env.add_plank(b2Vec2(12,5), b2Vec2(13,6.5))
env.add_plank(b2Vec2(13,6.5), b2Vec2(14,5))
env.add_plank(b2Vec2(11,6.25), b2Vec2(13,6.5))
env.add_plank(b2Vec2(9,6.25), b2Vec2(11,6.25))
env.add_plank(b2Vec2(7.25,6.25), b2Vec2(9,6.25))


env.init_graphics()
for i in range(1000):    
    env.draw()
    env.step()

ui = UI(env)

sim = False
while True:
    env.draw()
    ui.update(env.world)
    ui.draw()
    
    env.step() if sim else None

    for event in ui.events:
        if event.type == "quit":
            quit()

        elif event.type == "add-plank":
            print(f"env.add_plank{event.data}")
            env.add_plank(*event.data)

        elif event.type == "add-road":
            print(f"env.add_road{event.data}")
            env.add_road(*event.data)

        elif event.type == "sim":
            sim = True

        elif event.type == "remove":
            #TODO
            pass
