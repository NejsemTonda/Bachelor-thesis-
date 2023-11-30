from entity import IEntity
from Box2D import b2
import math


class Buildable(IEntity):
    def __init__(self, world, start, end, thickness, density, friction):
        mid = start + (end - start)/2
        a = mid-start
        angle = math.atan2(a[1], a[0])

        self.body = world.CreateDynamicBody(
            position = mid,
            angle = angle,
            fixtures = b2.fixtureDef(shape = b2.polygonShape(box=((start-end).length/2, thickness)),
                                    density = density,
                                    friction = friction,
            )
        ) 
        self.forces = 0

    def update(self, env):
        if self.forces > self.break_limit:
            for j in env.world.joints:
                if self.body == j.bodyA or self.body == j.bodyB:
                    env.world.DestroyJoint(j)
                    for joint, e1, e2 in env.joint_tuple:
                        if j == joint:
                            env.joint_tuple.remove((joint,e1,e2))
            for a in env.anchor_dic.values():
                if self in a.entities:
                    a.entities.remove(self)

            if self in env.roads:
                env.roads.remove(self)

            if self in env.planks:
                env.planks.remove(self)

            env.world.DestroyBody(self.body)
            self.body = None
