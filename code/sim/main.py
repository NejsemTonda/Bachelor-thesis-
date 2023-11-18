from environment import Environment

env = Environment()
env.add_ground(
    [(0,10), (10,10), (10,0)]
)
env.add_ground(
    [(40,10), (30,10), (30,0)]
)

env.add_anchor()
env.add_anchor()


while True:
    env.step()
    env.draw()
