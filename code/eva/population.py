from __future__ import annotations
from eva.agents import Agent
from typing import Callable



class Population:
    agents: list[Agent]
    size: int
    selection: Callable[[Population], Population]
    crossover: Callable[[Population], Population]
    mutation: Callable[[Population], Population]
    fitness: Callable[[Agent], float]

    def __init__(self, size, agent_init, selection, crossover, mutation, fitness):
        self.size = size
        self.agent_init = agent_init
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.fitness = fitness

        self.agents = [agent_init() for _ in range(self.size)]

    def generation(self):
        for a in self.agents:
            fitness(a)

        best = max(self.agents)
        self.population = self.selection(self.population)
        self.population = self.crossover(self.population)
        self.population = self.mutation(self.population)

        return best
