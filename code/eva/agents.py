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
	x_bounds = (0,40)
	y_bounds = (0,30)
	def __init__(self, level):
		self.clicks = [vec2(random.randint(*self.x_bounds), random.randint(*self.y_bounds)) for _ in range(10)]
		self.types = [random.choice([Type.plank, Type.road, Type.none]) for _ in range(9)]

	def __repr__(self):
		return f"clicks = {self.clicks}, types = {self.types}"
