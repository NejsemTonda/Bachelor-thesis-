from environment import Environment
from Box2D.b2 import vec2
#from .ui import UI

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

env.add_car(vec2(5,11+e), density=3)

env.add_road(vec2(10,10), vec2(20,10))
env.add_road(vec2(20,10), vec2(30,10))

# This bridge will break
env.add_plank(vec2(10,10), vec2(15,15))
env.add_plank(vec2(15,15), vec2(20,10))
env.add_plank(vec2(20,10), vec2(25,15))
env.add_plank(vec2(25,15), vec2(30,10))
env.add_plank(vec2(15,15), vec2(25,15))


# uncoments this to add muscle support so bridge wont brake
#env.add_plank(vec2(15,15), vec2(20,16))
#env.add_plank(vec2(20,16), vec2(20,14))
#env.add_plank(vec2(20,14), vec2(25,15))
#env.add_plank(vec2(25,15), vec2(20,16))
#env.add_plank(vec2(20,14), vec2(15,15))


goal = vec2(38,12)


env.init_graphics()
ui = UI(env.graphics)


sim = False
while True:
    if sim:
        env.step()

    ui.update(env.world)
    for event in ui.events:
        if event.type == "quit":
            quit()

        elif event.type == "add-plank":
            print(event.data)
            env.add_plank(*event.data)

        elif event.type == "add-road":
            env.add_road(*event.data)

        elif event.type == "sim":
            sim = True

        elif event.type == "remove":
            #TODO
            pass

    env.graphics.draw_circle(goal, (env.car.chasssis.position - goal).length, color=(255,0,0), hollow=True)
    env.graphics.draw_circle(goal, 0.1, color=(255,0,0))
    ui.draw()
    env.draw()
