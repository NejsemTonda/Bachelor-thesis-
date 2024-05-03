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

def run_experiemt(exp, name=None, title=None, save=False, args_list=None):
    def process_data(data_runs):
        data = {"Evaluation": [], "Fitness": [], "Run": []}
        for run_id, run in enumerate(data_runs):
            for i, r in enumerate(run):
                data["Evaluation"].append(r[0])
                data["Fitness"].append(r[1])
                data["Run"].append(run_id)
        return pd.DataFrame(data)
    
    random.seed(42)
    np.random.seed(42)

    if name is None:
        save = False
        name = "Unnamed"
    if title is None:
        title = name


    print(f"running experiment {name}")
    RUNS = 1
    data_runs = []

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(title)

    ax1.set_title("Minimal Distance")
    ax1.set_xlabel("Number of Fitness Evaluations")
    ax1.set_ylabel("Fitness")

    ax2.set_title("Bridge Cost")
    ax2.set_xlabel("Number of Fitness Evaluations")
    ax2.set_ylabel("Fitness")

    if args_list == None:
        args_list = [{}]

    for args in args_list:
        for _ in tqdm(range(RUNS)):
            data_runs.append(exp(**args))

        label = ",".join([k+"="+str(v) for k,v in args.items()])

        try:
            import pickle
            h = name+title+label
            with open(str(h)+".pkl", "wb") as file:
                pickle.dump(data_runs, file)
        except:
            print("could not save", h)

        
        df1 = process_data([[(x[0], x[1][0]) for x in run] for run in data_runs])
        df2 = process_data([[(x[0], x[1][1]) for x in run] for run in data_runs])
        


        sns.lineplot(df1, x="Evaluation", y="Fitness", label=label, ax=ax1)
        sns.lineplot(df2, x="Evaluation", y="Fitness", label=label, ax=ax2)

    ax1.legend()
    ax2.legend()

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

def simple(size=500, gens=200, l=25):
    level = LevelFactory.level1()
    fitness = partial(fits.simple_fitness, level=LevelFactory.level1)
    
    pop = Population(
        size,
        partial(agents.SimpleGenome.new, level, length=l),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1) ,
        partial(mut.simple),
        fitness,
    )

    res = []
    for _ in range(gens):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res

def polar_simple(size=500, gens=200, l=25):
    level = LevelFactory.level1()
    fitness = partial(fits.polar_fitness, level=LevelFactory.level1)
    
    pop = Population(
        size,
        partial(agents.PolarGenome.new, level, length=l),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
    )
    
    res = []
    for i in range(gens):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res

def improved_polar(size=500, gens=200, l=25, alpha=0.1, beta=0.1):
    level = LevelFactory.level1()
    fitness = partial(fits.improved_fitness, level=LevelFactory.level1, alpha=alpha, beta=beta)
    
    pop = Population(
        size,
        partial(agents.PolarGenome.new, level, length=l),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
    )

    res = []
    for _ in range(gens):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res

def elit(size=500, gens=200, l=25, elit=0.05):
    level = LevelFactory.level1()
    fitness = partial(fits.improved_fitness, level=LevelFactory.level1)
    
    pop = Population(
        size,
        partial(agents.PolarGenome.new, level, length=l),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
        elit=elit
    )

    res = []
    for _ in range(gens):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res



def increasing_hardness(size=500, gens=200, l=25, avg=5, increase=0.05):
    level = LevelFactory.level1()
    hardness = 0.9
    fitness = partial(fits.increasing_fitness, hardness=hardness, level=LevelFactory.level1)
    
    pop = Population(
        size,
        partial(agents.PolarGenome.new, level, length=l),
        partial(sel.tournament_selection),
        partial(cx.n_point, n=1),
        partial(mut.polar),
        fitness,
    )

    res = []
    for _ in range(gens):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))
        overall_fits = [a.fitness[0] for a in pop.agents]
        if sum(overall_fits)/len(overall_fits) > -avg:
            hardness += -increase
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
    

def graph_genome(size=500, gens=200, nodes=25):
    level = LevelFactory.level1()
    fitness = partial(fits.graph_fitness, level=LevelFactory.level1)
   
    pop = Population(
        size,
        partial(agents.GraphGenome.new, node_count=nodes, level=level),
        partial(sel.tournament_selection),
        partial(cx.graph_cx),
        partial(mut.graph),
        fitness,
        elit=0.05
    )

    res = []
    for _ in range(gens):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))

    return res

def graph_inc(size=500, gens=200, l=25, avg=5, increase=0.05):
    level = LevelFactory.level1()
    hardness = 0.9

    fitness = partial(fits.graph_increasing, hardness=hardness, level=LevelFactory.level1)
    pop = Population(
        size,
        partial(agents.GraphGenome.new, node_count=l, level=level),
        partial(sel.tournament_selection),
        partial(cx.graph_cx),
        partial(mut.graph),
        fitness,
    )


    res = []
    for _ in range(gens):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))
        overall_fits = [a.fitness[0] for a in pop.agents]
        if sum(overall_fits)/len(overall_fits) > -avg:
            hardness += -increase
            fitness = partial(fits.graph_increasing, hardness=hardness, level=LevelFactory.level1)
            pop.update_fitness(fitness)
            print("hardness increased")

    return res

def better_init(size=500, gens=200, l=25, omega=1):
    level = LevelFactory.level1()
    fitness = partial(fits.graph_fitness, level=LevelFactory.level1)
   
    pop = Population(
        size,
        partial(agents.GraphGenome.better_init, level, omega=omega),
        partial(sel.tournament_selection),
        partial(cx.graph_cx),
        partial(mut.graph),
        fitness,
        elit=0.05
    )
    
    res = []
    for _ in range(gens):
        pop.generation()
        res.append((pop.f_evaluations, pop.best.fitness))
        print(fitness(pop.best, draw=False))
        

    return res


if __name__ == "__main__":
    #run_experiemt(knapsack, "knap", "Knapsack Problem", save=True)
    run_experiemt(simple, "simple", "Jenoduché kódování jedince", args_list=[
        {"size": 500, "gens": 200, "l":20}, 
    ], save=True)
    run_experiemt(polar_simple, "polar-len", "Agent s polární reprezetací, různé délky genu", args_list=[
        {"l":10}, 
        {"l":20}, 
        {"l":50}, 
    ], save=True)
    run_experiemt(polar_simple, "polar-pop", "Agent s polárním kódováním, různé velikosti populace", args_list=[
        {"size": 500, "gens": 200}, 
        {"size": 1000, "gens": 100}, 
        {"size": 100, "gens": 1000}, 
    ], save=True)
    run_experiemt(improved_polar, "impolar", "Vylepšená fitness", args_list=[
        {"alpha": 0, "beta":0},
        {"alpha": 0.1, "beta":0},
        {"alpha": 0, "beta":0.1},
        {"alpha": 0.1, "beta":1},
        {"alpha": 1, "beta":0.1},
        {"alpha": 1, "beta":1},
    ], save=True)
    run_experiemt(elit, "elit", "Evoluce s eliticismem", args_list=[
        {"elit": 0},
        {"elit": 0.05},
        {"elit": 0.1},
        {"elit": 0.5},
        {"elit": 0.9},
    ], save=True)

    run_experiemt(increasing_hardness, "inc", "Měnící se fitness", args_list=[
        {"avg": 5, "increase": 0.05},
        {"avg": 0.5, "increase": 0.05},
        {"avg": 10, "increase": 0.05},
        {"avg": 5, "increase": 0.01},
        {"avg": 5, "increase": 0.1},
    ], save=True)

    run_experiemt(graph_genome, "graph", "Agent s grafovým kódováním", args_list=[
        {"nodes": 10},
        {"nodes": 20},
        {"nodes": 50},
    ], save=True)

    run_experiemt(graph_inc, "graph-inc", "Agent s grafovým kódováním a měnící se fitness", args_list=[
        {"avg": 5, "increase": 0.05},
        {"avg": 0.5, "increase": 0.05},
        {"avg": 10, "increase": 0.05},
        {"avg": 5, "increase": 0.01},
        {"avg": 5, "increase": 0.1},

    ], save=True)

    run_experiemt(better_init, "init", "Vylepšená inicializace", args_list=[
        {"omega": 1},
        {"omega": 0.5},
        {"omega": 0.1},
    ], save=True)
