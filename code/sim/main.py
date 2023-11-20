from environment import Environment
from Box2D.b2 import vec2
import pygame
from ui import UI

env = Environment()
e = 0.1
env.add_ground(
    [(0,10+e), (10,10+e), (10,0)],
    anchors=[vec2(10,10)] 
)
env.add_ground(
    [(40,10+e), (30,10+e), (30,0)],
    anchors=[vec2(30,10)] 
)

env.add_car(vec2(5,11+e))

env.add_road(vec2(10,10), vec2(20,10))
env.add_road(vec2(20,10), vec2(30,10))

env.add_plank(vec2(10,10), vec2(15,15))
env.add_plank(vec2(15,15), vec2(20,10))
env.add_plank(vec2(20,10), vec2(25,15))
env.add_plank(vec2(25,15), vec2(30,10))
env.add_plank(vec2(15,15), vec2(25,15))

env.init_graphics()

ui = UI(env.graphics)

while True:
    env.step()
    env.draw()

    ui.update(env.world)
    for event in ui.events:
        if event.type == "quit":
            quit()

        elif event.type == "add-plank":
            env.add_plank(*event.data)

        elif event.type == "add-road":
            env.add_road(*event.data)

        elif event.type == "remove":
            #TODO
            pass



