from eva.agents import Type
from Box2D.b2 import vec2 
import random

def simple(agents, click_p=0.1, click_max=1, type_p=0.05, type_weigths=[1,1,1]):
	types = [Type.plank, Type.road, Type.none]
	for a in agents:
		for i in range(len(a.genome.types)):
			if random.random() < type_p:
				a.genome.types[i] = random.choices(types, type_weigths)[0]
			if random.random() < click_p:
				a.genome.clicks[i] += vec2(random.randint(0,click_max),random.randint(0,click_max))

		if random.random() < click_p:
				a.genome.clicks[-1] += vec2(random.randint(0,click_max),random.randint(0,click_max))

	return agents
