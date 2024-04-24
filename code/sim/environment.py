from Box2D.b2 import vec2 
from Box2D import b2
from .helpers import VecDict, correctLen
from .components import Plank, Road, Car, Ground, Anchor

SCALER = 4
class Environment:
    def __init__(self,
            steps=60, #physical simulation steps per iterations
            max_plank_len=2.05,
            max_road_len=None,
            buildable_weight=1.3475121952552491, #buildable b2.density, found by rs
            buildable_limit=765, #limit fo b2.reaction force, found by rs
            road_weight_multiplier = 3.99204226720507, #how many times is road denser then plank, found by rs
            road_limit_multiplier = 0.8214835226562238, #how many times is road stronger then plank, found by rs
        ):
        if max_road_len is None: max_road_len = max_plank_len 
        self.graphics = None
        self.steps = steps
        self.grounds = []
        self.planks = []
        self.roads = []
        self.cars = []

        self.anchor_dic = VecDict()
        self.joint_tuple = []
        
        self.world = b2.world(gravity=(0, -10), doSleep=True)

        self.max_plank_len = max_plank_len
        self.max_road_len = max_road_len
        self.plank_weight = buildable_weight
        self.road_weight = road_weight_multiplier*self.plank_weight
        self.plank_limit = buildable_limit
        self.road_limit = self.plank_limit * road_limit_multiplier

        self.plank_pm_cost = 180
        self.road_pm_cost = 200

        self.cost = 0


    def add_plank(self, start, end):
        start = vec2(list(map(int,vec2(start)*SCALER)))/SCALER
        end = vec2(list(map(int,vec2(end)*SCALER)))/SCALER
        end1 = end
        end = correctLen(start, end, self.max_plank_len)
        #if end1 != end: print("edge was too long")
        self.cost += self.plank_pm_cost*(start-end).length
        plank = Plank(self.world, start, end, self.plank_limit, self.plank_weight)
        self.planks.append(plank)

        self.create_joints(plank, start, end)
        return plank


    def add_road(self, start, end):
        start = vec2(list(map(int,vec2(start)*SCALER)))/SCALER
        end = vec2(list(map(int,vec2(end)*SCALER)))/SCALER
        end1 = end
        end = correctLen(start, end, self.max_road_len)
        #if end1 != end: print("edge was too long")
        self.cost += self.road_pm_cost*(start-end).length
        road = Road(self.world, start, end, self.road_limit, self.road_weight)
        self.roads.append(road)

        self.create_joints(road, start, end)
        return road

    def create_joints(self, buildable, start, end):
        for pos in [start,end]:
            if not pos in self.anchor_dic:
                self.anchor_dic[pos] = self.add_anchor(pos)   
            anchor = self.anchor_dic[pos]

            j = self.world.CreateRevoluteJoint(
                bodyA=buildable.body,
                bodyB=anchor.body,
                anchor=pos,
            )

            self.joint_tuple.append((j, buildable))



    def add_ground(self, shape, anchors=[]):
        shape = list(map(vec2,shape))
        anchors = list(map(vec2,anchors))
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
        self.cars.append(c)
        return c

    def step(self):
        for e in self.roads+self.planks:
            e.forces = 0

        for joint, e in self.joint_tuple:
            e.forces += joint.GetReactionForce(self.steps).length

        for e in self.planks+self.roads:
            e.update(self)
        
        for c in self.cars:
            c.update(self)

        self.world.Step(1.0/self.steps, 6, 2)

    def init_graphics(self):
        from .graphics import Graphics
        self.graphics = Graphics(fps=120)

    def draw(self):
        if self.graphics == None:
            self.init_graphics()

        for e in self.grounds+self.planks+self.roads+list(self.anchor_dic.values()):
            e.draw(self.graphics)

        for c in self.cars:
            c.draw(self.graphics)

        self.graphics.draw()
