import eva.crossovers as cx
import eva.mutations as mut
import eva.fitness as fits
import eva.selections as sel
import eva.agents as agents
from eva.agents import Agent, Type
from eva.population import Population
from levels import LevelFactory
from functools import partial
import numpy as np
import random 
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt 
from tqdm import tqdm

def pol2cart(l, alpha):
        x = l * np.cos(alpha)
        y = l * np.sin(alpha)
        return(x, y)
from Box2D.b2 import vec2

def run_experiemt(exp, name=None, title=None, save=False):
    if name is None:
        save = False
        name = "Unnamed"

    if title is None:
        title = name

    RUNS = 3
    data_runs = []

    for _ in tqdm(range(RUNS)):
        data_runs.append(exp())

    data = {"Evaluation": [], "Max": [], "Min": [], "Mean": []}
    for i in range(len(data_runs[0])):  # Assuming all runs have the same length
       max_fitness_values = [run[i][1] for run in data_runs]
       data["Evaluation"].append(data_runs[0][i][0])
       data["Max"].append(max(max_fitness_values))
       data["Min"].append(min(max_fitness_values))
       data["Mean"].append(sum(max_fitness_values) / len(max_fitness_values))
    
    df = pd.DataFrame(data)
    
    # Plotting
    sns.lineplot(data=df, x="Evaluation", y="Mean", label="Mean")
    plt.fill_between(df["Evaluation"], df["Min"], df["Max"], alpha=0.2, label="Min-Max Range")
    plt.legend()
    plt.title(title)
    plt.xlabel("Number of Fitness Evaluations")
    plt.ylabel("Fitness")
    if save:
        plt.savefig("data/pictures/"+name+".pdf")
    else:
        plt.show()

def knapsack():
    with open("data/knapsack.txt", "r") as file:
        knapsack = eval(file.read())

    pop = Population(
        1000,
        partial(agents.KnapsackGenome.new, k_len=len(knapsack[0])),
        partial(sel.tournament_selection),
        partial(cx.knapsack_cx),
        partial(mut.knapsack),
        partial(fits.knapsack_fit, knapsack=knapsack),
        elit=0.01,
        parallel=False,
    )
    
    res = []
    for i in range(200):
        pop.generation()
        res.append((pop.fitness_evaluation, pop.best.fitness))
    
    return res

def simple():
    level = LevelFactory.level1()
    fitness = partial(fits.simple_fitness, level=LevelFactory.level1)
    
    pop = Population(
        100,
        partial(agents.SimpleGenome.new, level, length=10),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1) ,
        partial(mut.simple),
        fitness,
    )

    while True:
        pop.generation()
        print(pop.best)
        print(fitness(pop.best, draw=True))


def radians_simple():
    level = LevelFactory.level1()
    fitness = partial(fits.polar_fitness, level=LevelFactory.level1)
    
    pop = Population(
        100,
        partial(agents.PolarGenome.new, level, length=20),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
        elit=0.00
    )
    
    fitness(pop.best, draw=True)

    for i in range(200):
        pop.generation()
        if True: print(fitness(pop.best, draw=True))

def improved_radians():
    level = LevelFactory.level1()
    fitness = partial(fits.improved_fitness, level=LevelFactory.level1)
    
    pop = Population(
        1000,
        partial(agents.PolarGenome.new, level, length=20),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
        elit=0.05,
        parallel = True
    )
    fitness(pop.best, draw=True)

    for _ in range(200):
        pop.generation()
        print(len(pop.best.genome.clicks))
        if True: print(fitness(pop.best, draw=True))


def increasing_hardness():
    level = LevelFactory.level1()
    hardness = 0.9
    fitness = partial(fits.increasing_fitness, hardness=hardness, level=LevelFactory.level1)
    
    pop = Population(
        100,
        partial(agents.PolarGenome.new, level, length=20),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
        elit=0.00,
        parallel = True
    )

    for _ in range(200):
        pop.generation()
        overall_fits = [a.fitness for a in pop.agents]
        if True: print(fitness(pop.best, draw=True)) 
        print(sum(overall_fits)/len(overall_fits))
        if sum(overall_fits)/len(overall_fits) > -5:
            hardness += -0.05
            fitness = partial(fits.increasing_fitness, hardness=hardness, level=LevelFactory.level1)
            pop.fitness_f = fitness 
            print("hardness increased")


def graph_genome():
    level = LevelFactory.level1()
    fitness = partial(fits.graph_fitness, level=LevelFactory.level1)
   
    while True:
        pop = Population(
            1000,
            partial(agents.GraphGenome.new, level),
            partial(sel.tournament_selection),
            partial(cx.graph_cx, n=1),
            partial(mut.graph),
            fitness,
            elit=0.00,
            parallel = True
        )
        
        fitness(pop.best, draw=True)


if __name__ == "__main__":
    #random.seed(42)
    #np.random.seed(42)
    level = LevelFactory.level1()
    #run_experiemt(knapsack, "knap", "Knapsack Problem", save=False)
    #knapsack()
    #radians_simple()
    #simple()
    #improved_radians()
    #increasing_hardness()

    #fitness = partial(fits.improved_fitness, level=LevelFactory.level1)
    #a = Agent(agents.PolarGenome.new(level, length=20))
    #print(a)
    #print(fitness(a, draw=True))

    graph_genome()
    

    quit()
    simple()
