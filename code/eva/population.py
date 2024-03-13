from __future__ import annotations
from eva.agents import Agent
from typing import Callable
from tqdm import tqdm



class Population:
    agents: list[Agent]
    size: int
    selection: Callable[[Population], Population]
    crossover: Callable[[Population], Population]
    mutation: Callable[[Population], Population]
    fitness: Callable[[Agent], float]
    best: Agent

    def __init__(self, size, agent_init, selection, crossover, mutation, fitness):
        self.size = size
        self.agent_init = agent_init
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.fitness = fitness

        self.agents = [Agent(agent_init()) for _ in range(self.size)]

        for a in tqdm(self.agents):
            self.fitness(a)

        self.best = max(self.agents)

    def generation(self):
        self.agents = self.selection(self.agents)
        self.agents = self.crossover(self.agents)
        self.agents = self.mutation(self.agents)
        for a in tqdm(self.agents):
            self.fitness(a)

        self.best = max(self.agents)

        return self.best
