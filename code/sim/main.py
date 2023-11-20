from environment import Environment
from Box2D.b2 import vec2
import pygame

env = Environment()
env.add_ground(
    [(0,10), (10,10), (10,0)],
    anchors=[vec2(10,10)] 
)
env.add_ground(
    [(40,10), (30,10), (30,0)],
    anchors=[vec2(30,10)] 
)

env.add_car(vec2(5,11))

env.add_plank(vec2(10,10), vec2(20,10))
env.add_plank(vec2(20,10), vec2(30,10))

env.add_plank(vec2(10,10), vec2(15,15))
env.add_plank(vec2(15,15), vec2(20,10))
env.add_plank(vec2(20,10), vec2(25,15))
env.add_plank(vec2(25,15), vec2(30,10))
env.add_plank(vec2(15,15), vec2(25,15))



while True:
    env.step()
    env.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            quit()

