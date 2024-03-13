import crossovers
import mutations
import fitness
from agents import Agent, SimpleGenome,Type
from levels import LevelFactory
from Box2D.b2 import vec2
from tqdm import tqdm

level = LevelFactory.level1()
a = Agent(SimpleGenome(level))
b = Agent(SimpleGenome(level))
c = Agent(SimpleGenome(level))

c.genome.clicks = [vec2(10,10), vec2(20,10), vec2(30,10), vec2(25,15), vec2(20,10), vec2(15,15), vec2(10,10),vec2(15,15), vec2(25,15)]
c.genome.types = [Type.road, Type.road, Type.none, Type.none, Type.none, Type.none, Type.none, Type.none, Type.none]

fitness.simple_fitness(c, LevelFactory.level1(), draw=True)
quit()

agents = [Agent(SimpleGenome(level)) for _ in range(1000)]

fits = []
for a in tqdm(agents):
    fitness.simple_fitness(a, LevelFactory.level1())

best = min(agents)
print(best)
fitness.simple_fitness(best, LevelFactory.level1(), draw=True)


