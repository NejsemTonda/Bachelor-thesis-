import eva.crossovers
import eva.mutations
import eva.fitness
from eva.agents import Agent, SimpleGenome, Type
from levels import LevelFactory
from Box2D.b2 import vec2
from tqdm import tqdm


level = LevelFactory.level1()
a = Agent(SimpleGenome(level))
b = Agent(SimpleGenome(level))
c = Agent(SimpleGenome(level))

c.genome.clicks = [vec2(15,10), vec2(17,10), vec2(15,7), vec2(17,10), vec2(21,10), vec2(25,10), vec2(10,10),vec2(15,15), vec2(25,15)]
c.genome.types = [Type.road, Type.plank, Type.none, Type.road, Type.road, Type.none, Type.none, Type.none, Type.none]

eva.fitness.simple_fitness(c, LevelFactory.level1(), draw=True)
quit()

agents = [Agent(SimpleGenome(level, lenght=20)) for _ in range(1000)]

fits = []
for a in tqdm(agents):
	eva.fitness.simple_fitness(a, LevelFactory.level1())

best = min(agents)
print(best)
eva.fitness.simple_fitness(best, LevelFactory.level1(), draw=True)


