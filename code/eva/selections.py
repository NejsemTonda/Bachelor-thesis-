import random
import copy 
def tournament_selection(agents,k=10):
    offspring = [] 
    for _ in range(len(agents)):
        tournament = [random.choice(agents) for _ in range(k)]
        offspring.append(copy.deepcopy(max(tournament)))
    return offspring
