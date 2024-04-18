import random
from Box2D.b2 import vec2
from enum import Enum
import numpy as np

class Type(Enum):
    none = 0
    plank = 1
    road = 2

class Agent:
    def __init__(self, genome):
        self.fitness = None
        self.genome = genome

    def __repr__(self):
        return f"fitness: {self.fitness} from genome: {self.genome}"

    def __gt__(self, other):
        return self.fitness > other.fitness

class KnapsackGenome(list):
    def new(k_len):
        l = ["1" if random.random() < 0.5 else "0" for _ in range(k_len)]
        return KnapsackGenome(l)

    def __repr__(self):
        return "".join(self)

class SimpleGenome:
    def __init__(self, clicks, types):
        assert len(clicks) == len(types), f"lengths of clicks and types are mismatched {len(clicks)} {len(types)}"
        self.clicks = clicks
        self.types = types

    def new(level, length=20):
        clicks = [(
            random.randint(level.x_bounds[0]*4, level.x_bounds[1]*4)/4,
            random.randint(level.y_bounds[0]*4, level.y_bounds[1]*4)/4,
            ) for _ in range(length)
        ]
        types = random.choices([Type.plank, Type.road, Type.none], k=length)
        return SimpleGenome(clicks, types)

    def __repr__(self):
        return f"clicks = {self.clicks}, types = {self.types}"

class PolarGenome:
    def __init__(self, clicks, types):
        assert len(clicks) == len(types), f"lengths of clicks and types are mismatched {len(clicks)} {len(types)}"
        self.clicks = clicks
        self.types = types

    def new(level, length=20):
        clicks = [(level.env.max_plank_len*random.random(), random.random()*np.pi*2) for _ in range(length)]
        types = random.choices([Type.plank, Type.road, Type.none], k=length, weights=[1,1,0])
        return SimpleGenome(clicks, types)

    def __repr__(self):
        return f"clicks = {self.clicks}, types = {self.types}"


if __name__ == "__main__":
    g = KnapsackGenome.new(10)
