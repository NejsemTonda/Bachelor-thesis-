import random
def tournament_selection(agents,k=3):
    offspring = [] 
    for _ in range(len(agents)):
        tournament = [random.choice(agents) for _ in range(k)]
        offspring.append(max(tournament))
    return offspring
