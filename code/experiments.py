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
import copy
from Box2D.b2 import vec2

def run_experiemt(exp, name=None, title=None, save=False):
    def process_data(data_runs):
        data = {"Evaluation": [], "Max": [], "Min": [], "Mean": []}
        for i in range(len(data_runs[0])):  # Assuming all runs have the same length
            max_fitness_values = [run[i][1] for run in data_runs]
            data["Evaluation"].append(data_runs[0][i][0])
            data["Max"].append(max(max_fitness_values))
            data["Min"].append(min(max_fitness_values))
            data["Mean"].append(sum(max_fitness_values) / len(max_fitness_values))
        return pd.DataFrame(data)
    
    def plot_data(df, title, subplot):
        sns.lineplot(data=df, x="Evaluation", y="Mean", label="Average Best fitness", ax=subplot)
        subplot.fill_between(df["Evaluation"], df["Min"], df["Max"], alpha=0.2, label="Min-Max Range")
        subplot.legend()
        subplot.set_title(title)
        subplot.set_xlabel("Number of Fitness Evaluations")
        subplot.set_ylabel("Fitness")


    random.seed(42)
    np.random.seed(42)

    if name is None:
        save = False
        name = "Unnamed"
    if title is None:
        title = name

    print(f"running experiment {name}")
    RUNS = 3
    data_runs = []

    for _ in tqdm(range(RUNS)):
        data_runs.append(exp())

    df1 = process_data([[(x[0], x[1][0]) for x in run] for run in data_runs])
    df2 = process_data([[(x[0], x[1][1]) for x in run] for run in data_runs])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    plot_data(df1, "Minimal Distance", ax1)
    plot_data(df2, "Bridge Cost", ax2)

    plt.tight_layout()

    if save:
        plt.savefig(f"data/pictures/{name}.pdf")
    else:
        plt.show()
    plt.cla()

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
        parallel=False,
    )
    
    res = []
    for i in range(200):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))
    
    return res

def simple():
    level = LevelFactory.level1()
    fitness = partial(fits.simple_fitness, level=LevelFactory.level1)
    
    pop = Population(
        50,
        partial(agents.SimpleGenome.new, level, length=25),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1) ,
        partial(mut.simple),
        fitness,
    )

    res = []
    for _ in range(20):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res

def polar_simple():
    level = LevelFactory.level1()
    fitness = partial(fits.polar_fitness, level=LevelFactory.level1)
    
    pop = Population(
        50,
        partial(agents.PolarGenome.new, level, length=25),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
    )
    
    res = []
    for i in range(20):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res

def improved_polar():
    level = LevelFactory.level1()
    fitness = partial(fits.improved_fitness, level=LevelFactory.level1)
    
    pop = Population(
        50,
        partial(agents.PolarGenome.new, level, length=25),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
    )

    res = []
    for _ in range(20):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res

def elit():
    level = LevelFactory.level1()
    fitness = partial(fits.improved_fitness, level=LevelFactory.level1)
    
    pop = Population(
        50,
        partial(agents.PolarGenome.new, level, length=20),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
        elit=0.05
    )

    res = []
    for _ in range(20):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res



def increasing_hardness():
    level = LevelFactory.level1()
    hardness = 0.9
    fitness = partial(fits.increasing_fitness, hardness=hardness, level=LevelFactory.level1)
    
    pop = Population(
        50,
        partial(agents.PolarGenome.new, level, length=20),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
    )

    res = []
    for _ in range(20):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))
        overall_fits = [a.fitness for a in pop.agents]
        if sum(overall_fits)/len(overall_fits) > -5:
            hardness += -0.05
            fitness = partial(fits.increasing_fitness, hardness=hardness, level=LevelFactory.level1)
            pop.fitness_f = fitness 
            print("hardness increased")
    return res

def grap_mutations():
    while True:
        fitness = partial(fits.graph_fitness, level=LevelFactory.level1)
        nodes = [
            agents.GraphGenome.Node((6,5)),
            agents.GraphGenome.Node((8,5)),
            agents.GraphGenome.Node((10,5)),
            agents.GraphGenome.Node((12,5)),
            agents.GraphGenome.Node((14,5)),
            agents.GraphGenome.Node((7,6)),
            agents.GraphGenome.Node((9,6)),
            agents.GraphGenome.Node((11,6)),
            agents.GraphGenome.Node((13,6)),
        ]
        edges = [
            (nodes[0], nodes[1], Type.road), 
            (nodes[1], nodes[2], Type.road), 
            (nodes[2], nodes[3], Type.road), 
            (nodes[3], nodes[4], Type.road), 
            (nodes[0], nodes[5], Type.plank), 
            (nodes[5], nodes[1], Type.plank), 
            (nodes[1], nodes[6], Type.plank), 
            (nodes[6], nodes[2], Type.plank), 
            (nodes[2], nodes[7], Type.plank), 
            (nodes[7], nodes[3], Type.plank), 
            (nodes[3], nodes[8], Type.plank), 
            (nodes[8], nodes[4], Type.plank), 
            (nodes[5], nodes[6], Type.plank), 
            (nodes[6], nodes[7], Type.plank), 
            (nodes[7], nodes[8], Type.plank), 
        ]
        for e in edges:
            e[0].edges.append(e[1])
            e[1].edges.append(e[0])
        a = Agent(agents.GraphGenome(nodes, edges))
        a = mut.graph([a])[0]
        fitness(a, draw=True)
    

def graph_genome():
    level = LevelFactory.level1()
    fitness = partial(fits.graph_fitness, level=LevelFactory.level1)
   
    pop = Population(
        50,
        partial(agents.GraphGenome.new, level),
        partial(sel.tournament_selection),
        partial(cx.graph_cx, n=1),
        partial(mut.graph),
        fitness,
        parallel = True
    )

    res = []
    for _ in range(20):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res

def graph_inc():
    level = LevelFactory.level1()
    hardness = 0.9

    fitness = partial(fits.graph_increasing, hardness=hardness, level=LevelFactory.level1)
    pop = Population(
        50,
        partial(agents.GraphGenome.new, level),
        partial(sel.tournament_selection),
        partial(cx.graph_cx, n=1),
        partial(mut.graph),
        fitness,
    )


    res = []
    for _ in range(20):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))
        overall_fits = [a.fitness[0] for a in pop.agents]
        if sum(overall_fits)/len(overall_fits) > -5:
            hardness += -0.05
            fitness = partial(fits.graph_increasing, hardness=hardness, level=LevelFactory.level1)
            pop.update_fitness(fitness)
            print("hardness increased")

    return res

def better_init():
    level = LevelFactory.level1()
    fitness = partial(fits.graph_fitness, level=LevelFactory.level1)
   
    pop = Population(
        50,
        partial(agents.GraphGenome.better_init, level),
        partial(sel.tournament_selection),
        partial(cx.graph_cx, n=1),
        partial(mut.graph),
        fitness,
        elit=0.0,
    )
    
    res = []
    for _ in range(20):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res


if __name__ == "__main__":
    #run_experiemt(knapsack, "knap", "Knapsack Problem", save=True)
    #run_experiemt(simple, "simple", "Simple Agent Reprezetation", save=False)
    #run_experiemt(polar_simple, "polar", "Agent with polar reprezentation", save=True)
    #run_experiemt(improved_polar, "impolar", "Improved fitness", save=True)
    #run_experiemt(elit, "elit", "Evolution with elitism", save=True)
    #run_experiemt(increasing_hardness, "inc", "Increasing Hardness", save=True)
    run_experiemt(graph_genome, "graph", "Graph Encodings", save=True)
    run_experiemt(graph_inc, "graph_inc", "Graph Encodings+Increasing Hardness", save=True)
    run_experiemt(better_init, "init", "Better initialization", save=True)
