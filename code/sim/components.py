import math
from Box2D import b2
from buildable import Buildable
from entity import IEntity 

class Plank(Buildable):
    def __init__(self, world, start, end, break_limit=float("inf")):
        super().__init__(world, start, end) 
        self.break_limit = break_limit
        # TODO set flag for collision filtering
            
    def draw(self, graphics):
        graphics.draw_polygon(self.body, color = self.stress_color)


class Road(Buildable):
    def __init__(self, world, start, end, break_limit=float("inf")):
        super().__init__(world, start, end) 
        self.break_limit = break_limit
        # TODO set flag for collision filtering
            
    def draw(self, graphics):
        # TODO diferent drawing than plank
        graphics.draw_polygon(self.body, color = self.stress_color)


class Car(IEntity):
    def __init__(self, world, speed=10, density=1, wheel_size=0.4):
        # Create the car body
        self.wheel_size = wheel_size
        self.speed = speed
        self.chasssis = world.CreateDynamicBody(
            position=pos,
            fixtures = Box2D.b2.fixtureDef(
                shape=polygonShape(vertices=[
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
        circle_fixtureDef = Box2D.b2.fixtureDef(
            shape=circleShape(radius=self.wheel_size),
            density=density
        )

        self.wheel1 = world.CreateDynamicBody(
            position=car_body.position + (1, -1),
            fixtures=circle_fixtureDef,
        )
        
        self.wheel2 = world.CreateDynamicBody(
            position=car_body.position + (-1, -1),
            fixtures=circle_fixtureDef
        )
        
        # Create joints to attach wheels to the car body
        joint1 = world.CreateRevoluteJoint(
            bodyA=car_body,
            bodyB=wheel1,
            anchor=wheel1.position,
        )
        
        joint2 = world.CreateRevoluteJoint(
            bodyA=car_body,
            bodyB=wheel2,
            anchor=wheel2.position,
        )


    def upadte(self, env):
        self.wheel1.angularVelocity = -self.speed
        self.wheel2.angularVelocity = -self.speed

    def draw(self, graphics):
        graphics.draw_polygon(self.body)
        graphics.circle(wheel1.position, self.wheel_size)
        graphics.circle(wheel2.position, self.wheel_size)



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
    
