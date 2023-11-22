from Box2D.b2 import vec2 
from Box2D import b2
from helpers import VecDict, correctLen
from components import Plank, Road, Car, Ground, Anchor


class Environment:
    def __init__(self, steps=60):
        self.graphics = None
        self.ui = None
        self.steps = steps
        self.grounds = []
        self.planks = []
        self.roads = []
        self.car = None

        self.anchor_dic = VecDict()
        self.joint_tuple = []
        
        self.world = b2.world(gravity=(0, -10), doSleep=True)


    def add_plank(self, start, end, max_len=10):
        end = correctLen(start, end, max_len)
        plank = Plank(self.world, start, end)
        self.planks.append(plank)

        self.create_joints(plank, start, end)
        return plank


    def add_road(self, start, end, max_len=10):
        end = correctLen(start, end, max_len)
        road = Road(self.world, start, end)
        self.roads.append(road)

        self.create_joints(road, start, end)
        return road

    def create_joints(self, buildable, start, end):
        for pos in [start,end]:
            if not pos in self.anchor_dic:
                self.anchor_dic[pos] = self.add_anchor(pos)   
            anchor = self.anchor_dic[pos]

            for other in anchor.entities:
                j = self.world.CreateRevoluteJoint(
                    bodyA=buildable.body,
                    bodyB=other.body,
                    anchor=pos
                )
                self.joint_tuple.append((j, buildable, other))
                    
            anchor.entities.append(buildable)



    def add_ground(self, shape, anchors=[]):
        g = Ground(self.world, shape)
        self.grounds.append(g)
        for pos in anchors:
            a = self.add_anchor(pos)
            a.entities.append(g)
            self.anchor_dic[pos] = a
        return g

    def add_anchor(self, pos):
        a = Anchor(pos)
        if pos in self.anchor_dic:
            print(f"on pos {pos} was already anchor - replacing")

        self.anchor_dic[pos] = a
        return a 

    def add_car(self, pos, **kwargs):
        self.car = Car(self.world, pos, **kwargs) 

    def step(self):
        for e in self.roads+self.planks:
            e.forces = 0

        for joint, e1, e2 in self.joint_tuple:
            force = joint.GetReactionForce(self.steps).length
            e1.forces += force
            e2.forces += force

        for e in self.planks+self.roads:
            e.update(self)

        if self.car is not None:
            self.car.update(self)

        self.world.Step(1.0/self.steps, 6, 2)

    def init_graphics(self):
        from graphics import Graphics
        self.graphics = Graphics()

    def draw(self):
        if self.graphics == None:
            self.init_graphics()

        self.graphics.clear()
        for e in self.grounds+self.planks+self.roads+list(self.anchor_dic.values()):
            e.draw(self.graphics)

        if self.car is not None:
            self.car.draw(self.graphics)

        if self.ui is not None:
            self.ui.draw(self.graphics)

        self.graphics.draw()
