import eva.crossovers as cx
import eva.mutations as mut
import eva.fitness as fits
import eva.selections as sel
import eva.agents as agents
from eva.population import Population
from levels import LevelFactory
from functools import partial

import experiments

experiments.knapsack()


fitness = partial(fits.fitness_radians, level=LevelFactory.level1)
new = partial(agents.RadianGenome.new, level, length=20),

pop = Population(
    100,
    partial(agents.RadianGenome.new, level, length=20),
    partial(sel.tournament_selection),
    partial(cx.n_point, n=1) ,
    partial(mut.radian),
    fitness,
)


while True:
    pop.generation()
    print(fitness(pop.best, draw=True))
