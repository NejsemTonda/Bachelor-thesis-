import copy 
from eva.agents import Type


def simple_fitness(agent, level, draw=False):
	level = level()
	last_click = agent.genome.clicks[0]
	for c,t in zip(agent.genome.clicks[1:], agent.genome.types):
		try:
			if t == Type.none:
				last_click = c
			elif t == Type.plank:
				added = level.env.add_plank(last_click, c)
				last_click = added.end
				
			elif t == Type.road:
				added = level.env.add_road(last_click, c)
				last_click = added.end
		except AssertionError:
			pass


	min_d = float('inf')
	static = 0
	for _ in range(1000):
		level.env.step()
		if draw:
			level.env.draw()
		
		car = level.car.chassis
		if car.position.y < -10:
			break
		if car.linearVelocity.length < 0.01:
			static += 1
			if static > 15:
				break
		else:
			static = 0

		min_d = min(min_d, (car.position - level.goal).length)
	fitness = min_d
	agent.fitness = fitness
	return fitness
