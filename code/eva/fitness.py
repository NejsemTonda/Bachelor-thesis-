import copy 
from eva.agents import Type

def simple_fitness(agent, level, draw=False):
	last_click = agent.genome.clicks[0]
	for c,t in zip(agent.genome.clicks[1:], agent.genome.types):
		try:
			if t == Type.none:
				pass
			elif t == Type.plank:
				level.env.add_plank(last_click, c)
				
			elif t == Type.road:
				level.env.add_road(last_click, c)

		except AssertionError:
			pass

		last_click = c

	min_d = float('inf')
	for _ in range(1000):
		level.env.step()
		if draw:
			level.env.draw()
		
		car_pos = level.car.chassis.position
		if car_pos.y < -10:
			break
		min_d = min(min_d, (car_pos - level.goal).length)

	agent.fitness = min_d
	return min_d
