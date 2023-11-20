import math
from Box2D import b2
from buildable import Buildable
from entity import IEntity 


class Plank(Buildable):
    def __init__(self, world, start, end, break_limit=float("inf")):
        super().__init__(world, start, end) 
        self.break_limit = break_limit
        col_filter = b2.filter(categoryBits=0x0002, maskBits=0xFFF8)
        print(self.body.fixtures[0].filterData)
        self.body.fixtures[0].filterData = col_filter
        
            
    def draw(self, graphics):
        graphics.draw_polygon(self.body, color = self.stress_color)


class Road(Buildable):
    def __init__(self, world, start, end, break_limit=float("inf")):
        super().__init__(world, start, end) 
        self.break_limit = break_limit
        col_filter = b2.filter(categoryBits=0x0001, maskBits=0xFFFF)
        self.body.fixtures[0].filter = col_filter
            
    def draw(self, graphics):
        # TODO diferent drawing than plank
        graphics.draw_polygon(self.body, color = self.stress_color)


class Car(IEntity):
    def __init__(self, world, pos, speed=10, density=1, wheel_size=0.4):
        # Create the car body
        self.wheel_size = wheel_size
        self.speed = speed
        self.chasssis = world.CreateDynamicBody(
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
                density=density
            ),
        )
        
        # Create the wheels
        circle_fixtureDef = b2.fixtureDef(
            shape=b2.circleShape(radius=self.wheel_size),
            density=density
        )

        self.wheel1 = world.CreateDynamicBody(
            position=self.chasssis.position + (1, -1),
            fixtures=circle_fixtureDef,
        )
        
        self.wheel2 = world.CreateDynamicBody(
            position=self.chasssis.position + (-1, -1),
            fixtures=circle_fixtureDef
        )
        
        # Create joints to attach wheels to the car body
        joint1 = world.CreateRevoluteJoint(
            bodyA=self.chasssis,
            bodyB=self.wheel1,
            anchor=self.wheel1.position,
        )
        
        joint2 = world.CreateRevoluteJoint(
            bodyA=self.chasssis,
            bodyB=self.wheel2,
            anchor=self.wheel2.position,
        )

        col_filter = b2.filter(categoryBits=0x0003, maskBits=0xFFFD)
        self.chasssis.fixtures[0].filterData = col_filter
        self.wheel1.fixtures[0].filterData = col_filter
        self.wheel2.fixtures[0].filterData = col_filter


    def update(self, env):
        self.wheel1.angularVelocity = -self.speed
        self.wheel2.angularVelocity = -self.speed

    def draw(self, graphics):
        graphics.draw_polygon(self.chasssis)
        graphics.draw_circle(self.wheel1.position, self.wheel_size, color=(128, 128,128))
        graphics.draw_circle(self.wheel2.position, self.wheel_size, color=(128, 128,128))



class Ground(IEntity):
    def __init__(self, world, shape):
        self.body = world.CreateBody()
        self.body.CreateEdgeChain(shape)

    def update(self, world):
        pass

    def draw(self, graphics):
        graphics.draw_edgeshape(self.body) 


class Anchor(IEntity):
    def __init__(self, pos):
        self.pos = pos
        self.entities = []

    def update(self):
        #TODO do I even need to update this?
        pass

    def draw(self, graphics):
        graphics.draw_circle(self.pos, color=(230, 242, 64))
    