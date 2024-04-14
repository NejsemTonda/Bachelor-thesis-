import eva.crossovers as cx
import eva.mutations as mut
import eva.fitness as fits
import eva.selections as sel
import eva.agents as agents
from eva.population import Population
from levels import LevelFactory
from functools import partial
import numpy as np
import random 
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt 
from tqdm import tqdm


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
        print(fitness(pop.best, draw=True))


def radians_simple():
    level = LevelFactory.level1()
    fitness = partial(fits.simple_fitness, level=LevelFactory.level1)
    
    pop = Population(
        100,
        partial(agents.SimpleGenome.new, level, length=10),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.simple),
        fitness,
        elit=0.05
    )

    while True:
        pop.generation()
        fitness(pop.best, draw=True)


if __name__ == "__main__":
   #random.seed(42)
   #np.random.seed(42)
   #run_experiemt(knapsack, "knap", "Knapsack Problem", save=False)
   radians_simple()
