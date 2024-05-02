# Code for Bachelor these

## Content

* [Evolutionary part](./eva)
    * [agents](./eva/agents): All used agent reprezentations and their init functions
    * [crossovers](./eva/crossover): All crossover
    * [fitness](./eva/fitness): All kinds of fitness functions used
    * [mutations](./eva/mutations): All mutations
    * [population](./eva/population): Code hadnling the population
    * [selections](./eva/selections): selections (only tournament was used)
* [Simulation part](./sim)
    * [entity](./sim/): Abstact class for every component used in simulation
    * [buildable](./sim/): Abstract class for buildable components (planks, roads)
    * [components](./sim/): All components in simulation (plank, road, ground, car, ...)
    * [environment](./sim/): Physical environment and its api
    * [graphics](./sim/): Code handling all graphics
* [UI](./sim/ui): Simple user interface for simulation
* [Levels](./level): Premade 4 levels from poly bridge
* [Experiments](./experiments): All experiments from thesis


### UI controls

The UI element has multiple different operation mode:
* press `p` to switch to `add-plank` mode
* press `r` to switch to `add-road` mode

When `add-plank` or `add-road` mode:
* left-click anywhere to select start position
* next left-click will select end position and add road or plank immidiately to the enviroment

Anytime:
* press `s` to start the simulation


### Using this code

If you are intrested in using this code for feel free to download and modify anything. Here follows simple usage

#### Creating an environment

A simple simulation could look like this:

```python
from sim.environment import Environment

env = Environment()

end.add_ground([(0,0), (10, 0), ...], anchors=[(0,0)]) # this will create solid ground from (0,0) to (10,0) with one anchor at (0,0)

env.add_plank((1,1), (1,3)) # this will add plank from (1,1) to (1,3)
env.add_road((2,1), (2,3)) # this will add road from (2,1) to (2,3)

env.add_car((3,3))  # this will add car to position (3,3)

while True:
    env.step() #this will run the simulation 
```

It might be easier to use one of the premade levels

```python
level = LevelFactory.level1()
env = level.env

while True:
    env.step()
```

If you wish to see whats is happening you must init graphics first


```python
level = LevelFactory.level1()
env = level.env
   
env.init_graphics()

while True:
    env.draw()
    env.step()
```

#### UI

You can find an example usage of simple UI in [`editor.py`](./editor.py)


#### Evolutionary Algorithms

If you wish to use my implementation of evolutionary algorithms, here is simple template

```python
from eva.population import Population 

pop = Population(
        1000, # size of population
        agent_init, # this function must produce eva.agents.Agent with you custom genome
        selection, # this function take one argument of type list[eva.agents.Agent] and must return list[eva.agents.Agent] with you custom selection
        xover, # same type hinting as with selection but with your custom crossover,
        mut, # same type hinting as with selection but with your mutation
        fitness, # you fitness, takes eva.agents.Agent and return anything that is comparable with <
)

for _ in range(200): # generations
    pop.generation()
    print(pop.best.fitness) # prints fitness of best ind. from population
    fitnesses = [a.fitness for a in pop.agents] # gets fitness of all agents in population 
```

#### Inspiration

Feel free to take inspiration from anything inside this repository. If  you wish to see how I have done my experiments look inside `experiments.py`
