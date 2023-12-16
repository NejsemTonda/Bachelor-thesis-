import math
from Box2D import b2
from .buildable import Buildable
from .entity import IEntity 


class Plank(Buildable):
	def __init__(self, world, start, end, break_limit, density=0.1, thickness=0.1, friction=1):
		super().__init__(world, start, end, thickness, density, friction) 
		self.break_limit = break_limit
		col_filter = b2.filter(maskBits=0x0)
		self.body.fixtures[0].filterData = col_filter
		
	def draw(self, graphics):
		rel_stress = min(1, self.forces/self.break_limit)
		stress_color = (255*rel_stress, 255*(1-rel_stress), 0)
		graphics.draw_polygon(self.body, color = stress_color)


class Road(Buildable):
	def __init__(self, world, start, end, break_limit, density=0.3, thickness=0.1, friction=1):
		super().__init__(world, start, end, thickness, density, friction) 
		self.break_limit = break_limit
		col_filter = b2.filter(categoryBits=0x0002, maskBits=0x0004)
		self.body.fixtures[0].filterData = col_filter
			
	def draw(self, graphics):
		# TODO diferent drawing than plank
		rel_stress = min(1, self.forces/self.break_limit)
		stress_color = (255*rel_stress, 0, 255*(1-rel_stress))
		graphics.draw_polygon(self.body, color = stress_color)


class Car(IEntity):
	def __init__(self, world, pos, speed=10, density=1, wheel_size=0.4):
		# Create the car body
		self.wheel_size = wheel_size
		self.speed = speed
		col_filter = b2.filter(categoryBits=0x0004, maskBits=0x000A)

		self.chassis = world.CreateDynamicBody(
			position=pos,
			fixtures = b2.fixtureDef(
				shape=b2.polygonShape(vertices=[
					(-1.5, -0.5),
					(1.5, -0.5),
					(1.5, 0.0),
					(0.0, 0.9),
					(-1.15, 0.9),
					(-1.5, 0.2),
				]),
				filter=col_filter,
				density=density
			),
		)
		
		# Create the wheels
		circle_fixtureDef = b2.fixtureDef(
			shape=b2.circleShape(radius=self.wheel_size),
			density=density,
			filter=col_filter,
		)

		self.wheel1 = world.CreateDynamicBody(
			position=self.chassis.position + (1, -1),
			fixtures=circle_fixtureDef,
		)
		
		self.wheel2 = world.CreateDynamicBody(
			position=self.chassis.position + (-1, -1),
			fixtures=circle_fixtureDef
		)
		
		# Create joints to attach wheels to the car body
		joint1 = world.CreateRevoluteJoint(
			bodyA=self.chassis,
			bodyB=self.wheel1,
			anchor=self.wheel1.position,
		)
		
		joint2 = world.CreateRevoluteJoint(
			bodyA=self.chassis,
			bodyB=self.wheel2,
			anchor=self.wheel2.position,
		)


	def update(self, env):
		self.wheel1.angularVelocity = -self.speed
		self.wheel2.angularVelocity = -self.speed

	def draw(self, graphics):
		graphics.draw_polygon(self.chassis)
		graphics.draw_circle(self.wheel1.position, self.wheel_size, color=(128, 128,128))
		graphics.draw_circle(self.wheel2.position, self.wheel_size, color=(128, 128,128))



class Ground(IEntity):
	def __init__(self, world, shape):
		self.body = world.CreateBody()
		self.body.CreateEdgeChain(shape)
		col_filter = b2.filter(categoryBits=0x0008, maskBits=0x0004)
		for fixture in self.body.fixtures:
			fixture.filterData = col_filter
		self.forces = 0

	def update(self, world):
		sefl.forces = 0

	def draw(self, graphics):
		graphics.draw_edgeshape(self.body) 


class Anchor(IEntity):
	def __init__(self, world, pos):
		self.pos = pos
		self.body = world.CreateDynamicBody(
			position=pos,
			fixtures = b2.fixtureDef(
				shape=b2.circleShape(radius=1),
				density=0,
				filter=b2.filter(categoryBits=0x00016, maskBits=0x0000)
			),
		)

	def update(self):
		pass

	def draw(self, graphics):
		graphics.draw_circle(self.pos, color=(230, 242, 64))
	
