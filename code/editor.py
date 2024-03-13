import sys
from sim.environment import Environment
from sim.ui import UI
from Box2D.b2 import vec2
from levels import LevelFactory
import random 



env = Environment()
e = 0.1
env.add_ground(
    [(0,10+e), (10,10+e), (10,0)],
    anchors=[vec2(10,10)] 
)
env.add_ground(
    [(40,10+e), (30,10+e), (30,0)],
    anchors=[vec2(30,10), vec2(20,30)] 
)
#car = env.add_car(vec2(5,11+e), density=30)

#env.add_road(vec2(10,10), vec2(22,10))
#env.add_road(vec2(14,10), vec2(22,10))
#r = env.add_road(vec2(18,10), vec2(25,10))
#env.add_road(vec2(22,10), vec2(29,10))
#env.add_road(vec2(26,10), vec2(30,10))
#
#env.add_plank(vec2(12,13), vec2(14,10))
#env.add_plank(vec2(14,10), vec2(16,13))
#env.add_plank(vec2(16,13), vec2(18,10))
#env.add_plank(vec2(18,10), vec2(20,13))
#env.add_plank(vec2(20,13), vec2(22,10))
#env.add_plank(vec2(22,10), vec2(24,13))
#env.add_plank(vec2(24,13), vec2(26,10))
#env.add_plank(vec2(26,10), vec2(28,13))
#env.add_plank(vec2(28,13), vec2(30,10))
#env.add_plank(vec2(12,13), vec2(10,10))
#env.add_plank(vec2(12,13), vec2(16,13))
#env.add_plank(vec2(16,13), vec2(20,13))
#env.add_plank(vec2(20,13), vec2(24,13))
#env.add_plank(vec2(24,13), vec2(28,13))



lvl = LevelFactory.test()
env = lvl.env
car = lvl.car
env.add_road(vec2(12,10), vec2(16,10))
env.add_road(vec2(16,10), vec2(20,10))
env.add_road(vec2(20,10), vec2(24,10))
env.add_road(vec2(24,10), vec2(38,10))

env.add_plank(vec2(12,6),  vec2(14,8))
env.add_plank(vec2(14,8),  vec2(16,10))
env.add_plank(vec2(14,8),  vec2(12,10))
env.add_plank(vec2(28,6),  vec2(26,8))
env.add_plank(vec2(26,8),  vec2(24,10))
#env.add_plank(vec2(26,8),  vec2(28,10))
#env.add_plank(vec2(24,10), vec2(20,13))
#env.add_plank(vec2(20,10), vec2(21,12))
#env.add_plank(vec2(20,10), vec2(19,12))
#env.add_plank(vec2(19,12), vec2(16,10))
#env.add_plank(vec2(19,12), vec2(21,12))


env.init_graphics()
ui = UI(env.graphics)

sim = True
while True:
    env.draw()
    ui.update(env.world)
    ui.draw()
    
    env.step() if sim else None

    for event in ui.events:
        if event.type == "quit":
            quit()

        elif event.type == "add-plank":
            print(event.data)
            env.add_plank(*event.data)

        elif event.type == "add-road":
            print(event.data)
            env.add_road(*event.data)

        elif event.type == "sim":
            sim = True

        elif event.type == "remove":
            #TODO
            pass
