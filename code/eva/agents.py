import random
from Box2D.b2 import vec2
from enum import Enum

class Type(Enum):
    none = 0
    plank = 1
    road = 2

class Agent():
    def __init__(self, genome):
        self.fitness = None
        self.genome = genome

    def __repr__(self):
        return f"fitness: {self.fitness} from genome: {self.genome}"

    def __gt__(self, other):
        return self.fitness > other.fitness
    
    def pickle(self):
        self.genome = SimpleGenome(
            list(map(lambda x: (x[0], x[1]),self.genome.clicks)),
            self.genome.types
        )
        
    def load(self):
        self.genome = SimpleGenome(
            list(map(lambda x: vec2(x[0], x[1]),self.genome.clicks)),
            self.genome.types
        )

class SimpleGenome:
    def __init__(self, clicks, types):
        assert len(clicks) == len(types)+1, f"lengths of clicks and types are mismatched {len(clicks)} {len(types)}"
        self.clicks = clicks
        self.types = types

    def new(level, length=20):
        first_anchor = list(level.env.anchor_dic.keys())[0]
        clicks = [(first_anchor)] + [(random.randint(*level.x_bounds), random.randint(*level.y_bounds)) for _ in range(length)]
        types = [random.choice([Type.plank, Type.road, Type.none]) for _ in range(length)]
        return SimpleGenome(clicks, types)

    def __repr__(self):
        return f"clicks = {self.clicks}, types = {self.types}"
