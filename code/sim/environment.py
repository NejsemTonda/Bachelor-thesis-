from Box2D.b2 import vec2 
from Box2D import b2
from helpers import VecDict
from components import Plank, Road, Car, Ground, Anchor


class Environment:
    def __init__(self):
        self.graphics = None
        self.grounds = []
        self.planks = []
        self.roads = []
        self.car = None
        self.anchor_dic = VecDict()
        self.joint_tuple = []
        
        self.world = b2.world(gravity=(0, -10), doSleep=True)


    def add_plank(self, start, end):
        plank = Plank(self.world, start, end)
        self.planks.append(plank)
        for pos in [start,end]:
            if not pos in self.anchor_dic:
                print(f"pos was not found, add new anchor at {pos}")
                self.anchor_dic[pos] = self.add_anchor(pos)
            else:
                print(f"anchor at {pos} was found it contains:")
                anchor = self.anchor_dic[pos]
                for e in anchor.entities:
                    print(e)
                
            
            anchor = self.anchor_dic[pos]

            for other in anchor.entities:
                print("added joint")
                j = self.world.CreateRevoluteJoint(
                    bodyA=plank.body,
                    bodyB=other.body,
                    anchor=pos
                )
                self.joint_tuple.append((j, plank, other))
                    
            anchor.entities.append(plank)

        return plank


    def add_road(self, start, end):
        # TODO implement adding road
        r = Road(self.world, start, end)
        self.roads.append(r)
        return r

    def add_ground(self, shape, anchors=[]):
        # TODO 
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

    def add_car(self, pos):
        self.car = Car(self.world, pos) 


    def step(self):
        self.world.Step(1.0/60, 6, 2)

    def draw(self):
        if self.graphics == None:
            from graphics import Graphics
            self.graphics = Graphics()

        self.graphics.clear()
        #print(self.grounds)
        #print(self.planks)
        #print(self.roads)
        #print(list(self.anchor_dic.values()))
        for e in self.grounds+self.planks+self.roads+list(self.anchor_dic.values()):
            e.draw(self.graphics)

        self.car.draw(self.graphics)
        self.car.update(self)


        self.graphics.draw()
        
