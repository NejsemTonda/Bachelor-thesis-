from entity import IEntity
from Box2D import b2


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
        self.start_joint = None
        self.end_joint = None
        for body in joint_dict[start]:
            self.start_joint = world.CreateRevoluteJoint(
                bodyA = body,
                bodyB = self.body,
                anchor = start
            )

        for body in joint_dict[end]:
            self.end_joint = world.CreateRevoluteJoint(
                bodyA = body,
                bodyB = self.body,
                anchor = end
            )


    def update(self, env):
        forces = 0 #TODO update force according to env
        c = min(self.forces, self.break_limit)/self.break_limit
        self.stress_color = (255*c, 255*(1-c), 0)

        if forces > self.break_limit:
            #TODO remove buildable
            pass 
