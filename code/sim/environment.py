from Box2D.b2 import vec2 
from Box2D import b2
from helpers import VecDict
from components import Plank, Road, Car


class Environment:
    def __init__(self):
        self.graphics = None
        self.grounds = []
        self.planks = []
        self.roads = []
        self.car = None
        self.joint_dic = VecDict()
        
        self.world = b2.world(gravity=(0, -10), doSleep=True)


    def add_plank(self, start, end):
        # TODO implement add plank
        p = Plank(self.world, start, end)

    def add_road(self, start, end):
        # TODO implement adding road
        r = Road(self.world, start, end)


    def add_ground(self, shape):
        # TODO 
        g = self.world.CreateBody()
        g.CreateEdgeChain(shape)
        pass

    def step(self):
        world.Step(1.0/60, 6, 2)
        pass

    def draw(self):
        if self.graphics == None:
            from graphics import Graphics
            self.graphics = Graphics()

        graphics.clear()
        for e in self.grounds+self.planks+self.roads:
            e.draw(graphics)

        graphics.draw()
        
