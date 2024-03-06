from sim.environment import Environment
from sim.components import Car
from Box2D.b2 import vec2
from dataclasses import dataclass

@dataclass
class Level:
	env: Environment
	car: Car
	goal: vec2
	x_bounds: vec2
	y_bounds: vec2



class LevelFactory:
	def level1():
		env = Environment()
		e = 0.1
		env.add_ground(
			[(0,10+e), (15,10+e), (15,0)],
			anchors=[vec2(15,10), vec2(15, 7)] 
		)
		env.add_ground(
			[(40,10+e), (25,10+e), (25,0)],
			anchors=[vec2(25,10), vec2(25, 7)] 
		)
		
		car = env.add_car(vec2(5,11+e), density=3)

		goal = vec2(38,12)

		x_bounds = (0,40)
		y_bounds = (0,30)

		return Level(env, car, goal, x_bounds, y_bounds)
