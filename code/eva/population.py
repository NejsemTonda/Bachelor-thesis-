from __future__ import annotations
from eva.agents import Agent
from typing import Callable
from tqdm import tqdm
import random
from multiprocessing import Pool
import copy



class Population:
    agents: list[Agent]
    size: int
    selection: Callable[[Population], Population]
    crossover: Callable[[Population], Population]
    mutation: Callable[[Population], Population]
    fitness_f: Callable[[Agent], float]
    best: Agent
    parallel: bool

    def __init__(self, size, agent_init, selection, crossover, mutation, fitness_f, elit=0, parallel=True):
        self.size = size
        self.agent_init = agent_init
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.fitness_f = fitness_f
        self.parallel = parallel
        self.elit = elit
        self.f_evaluations = 0

        self.agents = [Agent(agent_init()) for _ in range(self.size)]

        self._eval_fitness(self.agents)
        
        self.agents = sorted(self.agents, reverse=True)
        self.best = self.agents[0]

    def update_fitness(self, new_f):
        self.fitness_f = new_f
        self._eval_fitness(self.agents)

    def _eval_fitness(self, agents):
        if self.parallel:
            with Pool(6) as p:
                r = list(tqdm(p.imap(self.fitness_f, agents), total=len(agents)))
            
            for a,f in zip(agents,r):
                a.fitness = f
        else:
            for a in tqdm(agents):
                a.fitness = self.fitness_f(a)

        self.f_evaluations += len(agents)

    def generation(self):
        offspring = copy.deepcopy(self.agents)
        offspring = self.selection(offspring)
        offspring = self.crossover(offspring)
        offspring = self.mutation(offspring)

        self._eval_fitness(offspring)

        self.agents = offspring + self.agents[:int(len(self.agents) * self.elit)]
        self.agents = sorted(self.agents, reverse=True)[:self.size]
        self.best = self.agents[0]
