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

#c.genome.clicks = [vec2(10,10), vec2(20,10), vec2(30,10), vec2(25,15), vec2(20,10), vec2(15,15), vec2(10,10),vec2(15,15), vec2(25,15)]
#c.genome.types = [Type.road, Type.road, Type.plank, Type.plank, Type.plank, Type.plank, Type.plank, Type.plank, Type.plank]
c.genome.clicks = [vec2(37,21), vec2(39,10), vec2(33,3), vec2(40,23), vec2(38,12), vec2(6,23), vec2(8,9), vec2(35,29), vec2(16,5), vec2(4,15)]
c.genome.types = [Type.none, Type.plank, Type.none, Type.road, Type.plank, Type.road, Type.road, Type.road, Type.plank]
print(len(c.genome.clicks))
print(len(c.genome.types))

fitness.simple_fitness(c, LevelFactory.level1(), draw=True)
quit()

agents = [Agent(SimpleGenome(level)) for _ in range(100)]

fits = []
for a in tqdm(agents):
	fitness.simple_fitness(a, LevelFactory.level1())

best = min(agents)
print(best)
fitness.simple_fitness(best, LevelFactory.level1(), draw=True)


