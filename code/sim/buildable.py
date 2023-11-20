from entity import IEntity
from Box2D import b2
import math


class Buildable(IEntity):
    def __init__(self, world, start, end):
        mid = start + (end - start)/2
        a = mid-start
        angle = math.atan2(a[1], a[0])

        self.body = world.CreateDynamicBody(
            position = mid,
            angle = angle,
            fixtures = b2.fixtureDef(shape = b2.polygonShape(box=((start-end).length/2, 0.1)),
                                    density = 1,
                                    friction = 1
            )
        ) 
        self.forces = 0

    def update(self, env):
        if self.forces > self.break_limit:
            #TODO remove buildable
            pass 

