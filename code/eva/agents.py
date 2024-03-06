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


class SimpleGenome:
	def __init__(self, clicks, types):
		assert len(clicks) == len(types)+1, f"lengths of clicks and types are mismatched {len(clicks)} {len(types)}"
		self.clicks = clicks
		self.types = types

	def new(level, length=20):
		clicks = [vec2(random.randint(*level.x_bounds), random.randint(*level.y_bounds)) for _ in range(length)]
		types = [random.choice([Type.plank, Type.road, Type.none]) for _ in range(length-1)]
		return SimpleGenome(clicks, types)
	def __repr__(self):
		return f"clicks = {self.clicks}, types = {self.types}"
