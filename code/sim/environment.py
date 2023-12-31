from Box2D.b2 import vec2 
from Box2D import b2
from .helpers import VecDict, correctLen
from .components import Plank, Road, Car, Ground, Anchor


class Environment:
	def __init__(self, steps=60):
		self.graphics = None
		self.steps = steps
		self.grounds = []
		self.planks = []
		self.roads = []
		self.car = None

		self.anchor_dic = VecDict()
		self.joint_tuple = []
		
		self.world = b2.world(gravity=(0, -10), doSleep=True)

		self.max_plank_len = 4
		self.max_road_len = 4
		self.plank_weight = 1
		self.road_weight = 6.4*self.plank_weight
		self.plank_limit = 800000
		self.road_limit = 900000


	def add_plank(self, start, end):
		end = correctLen(start, end, self.max_plank_len)
		plank = Plank(self.world, start, end, self.plank_limit, self.plank_weight)
		self.planks.append(plank)

		self.create_joints(plank, start, end)
		return plank


	def add_road(self, start, end):
		end = correctLen(start, end, self.max_road_len)
		road = Road(self.world, start, end, self.road_limit, self.road_weight)
		self.roads.append(road)

		self.create_joints(road, start, end)
		return road

	def create_joints(self, buildable, start, end):
		for pos in [start,end]:
			if not pos in self.anchor_dic:
				self.anchor_dic[pos] = self.add_anchor(pos)   
			anchor = self.anchor_dic[pos]

			j = self.world.CreateRopeJoint(
				bodyA=buildable.body,
				bodyB=anchor.body,
				maxLength=0,
				localAnchorA=buildable.body.position-pos,
				localAnchorB=(0,0),
			)

			self.joint_tuple.append((j, buildable))



	def add_ground(self, shape, anchors=[]):
		g = Ground(self.world, shape)
		self.grounds.append(g)
		for pos in anchors:
			a = self.add_anchor(pos)
			a.body = g.body
			self.anchor_dic[pos] = a
		return g

	def add_anchor(self, pos):
		a = Anchor(self.world, pos)
		self.anchor_dic[pos] = a
		return a 

	def add_car(self, pos, **kwargs):
		c = Car(self.world, pos, **kwargs) 
		self.car = c
		return c

	def step(self):
		for e in self.roads+self.planks:
			e.forces = 0

		for joint, e in self.joint_tuple:
			e.forces += joint.GetReactionForce(self.steps).length

		for e in self.planks+self.roads:
			e.update(self)

		if self.car is not None:
			self.car.update(self)

		self.world.Step(1.0/self.steps, 6, 2)

	def init_graphics(self):
		from .graphics import Graphics
		self.graphics = Graphics()

	def draw(self):
		if self.graphics == None:
			self.init_graphics()

		for e in self.grounds+self.planks+self.roads+list(self.anchor_dic.values()):
			e.draw(self.graphics)

		if self.car is not None:
			self.car.draw(self.graphics)


		self.graphics.draw()
