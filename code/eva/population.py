from __future__ import annotations
from eva.agents import Agent
from typing import Callable
from tqdm import tqdm
import random
from multiprocessing import Pool



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

        self.agents = [Agent(agent_init()) for _ in range(self.size)]

        if self.parallel:
            with Pool(6) as p:
                r = list(tqdm(p.imap(self.fitness_f, self.agents), total=len(self.agents)))
            
            for a,f in zip(self.agents,r):
                a.fitness = f
        else:
            for a in tqdm(self.agents):
                a.fitness = self.fitness_f(a)

        self.fitness_evaluation = size

        self.agents = sorted(self.agents, reverse=True)
        self.best = self.agents[0]

    def generation(self):
        offspring = self.selection(self.agents)
        offspring = self.crossover(offspring)
        offspring = self.mutation(offspring)

        if self.parallel:
            with Pool(6) as p:
                r = list(tqdm(p.imap(self.fitness_f, offspring), total=len(offspring)))
            
            for a,f in zip(offspring,r):
                a.fitness = f
        else:
            for a in tqdm(offspring):
                a.fitness = self.fitness_f(a)

        self.fitness_evaluation += len(offspring)

        self.agents = offspring + self.agents[:int(len(self.agents) * self.elit)]
        self.agents = sorted(self.agents, reverse=True)[:self.size]
        self.best = self.agents[0]
