import sys
from sim.environment import Environment
from sim.ui import UI
from Box2D.b2 import vec2
from Box2D import b2Vec2
from levels import LevelFactory
import random 

import numpy as np


level = LevelFactory.level4()
env = level.env
   
env.init_graphics()

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
            run = False
            sim = True

        elif event.type == "remove":
            #TODO
            pass
