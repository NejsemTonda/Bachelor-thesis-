import eva.crossovers as cx
import eva.mutations as mut
import eva.fitness as fits
import eva.selections as sel
from eva.population import Population
from eva.agents import Agent, SimpleGenome, Type
from levels import LevelFactory
from Box2D.b2 import vec2
from tqdm import tqdm
from functools import partial


level = LevelFactory.level1()
foo = partial(SimpleGenome.new, level, length=20)

f = partial(fits.simple_fitness, level=LevelFactory.level1),
a = Agent(SimpleGenome(
	[vec2(0,0),vec2(0,0),vec2(0,0),vec2(0,0),vec2(0,0)]



pop = Population(
	100,
	partial(SimpleGenome.new, level, length=20),
	partial(sel.tournament_selection),
	partial(cx.n_point, n=1) ,
	partial(mut.simple),
	partial(fits.simple_fitness, level=LevelFactory.level1),
)

bests = []
for i in range(50):
	b = pop.generation()
	print(b.fitness)
	fits.simple_fitness(b, LevelFactory.level1, draw=True)
