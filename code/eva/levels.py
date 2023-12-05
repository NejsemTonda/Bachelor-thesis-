from ..sim.environment import Environment
from Box2D.b2 import vec2
from dataclasses import dataclass

@dataclass
class Level:
	env: Enviroment
	car: Car
	goal: vec2



class LevelFactory:
	def level1():
		env = Environment()
		e = 0.1
		env.add_ground(
			[(0,10+e), (10,10+e), (10,0)],
			anchors=[vec2(10,10)] 
		)
		env.add_ground(
			[(40,10+e), (30,10+e), (30,0)],
			anchors=[vec2(30,10)] 
		)
		
		car = env.add_car(vec2(5,11+e), density=3)

		goal = vec2(38,12)

		return Level(env, car, goal)
