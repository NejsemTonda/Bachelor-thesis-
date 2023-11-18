import math
from Box2D import b2
class Plank:
    def __init__(self, world, joint_dict, start, end):
        mid = start + (end - start)/2
        a = mid-start
        angle = math.atan2(a[1], a[0])

        self.body = world.CreateDynamicBody(
            position = mid,
            angle = angle,
            fixtures = b2.fixtureDef(shape = b2.polygonShape(box=((start-end).length/2, 0.25)),
                                    density = 1,
                                    friction = 1
            )
        ) 
        
        for body in joint_dict[start]:
            world.CreateRevoluteJoint(
                bodyA = body,
                bodyB = self.body,
                anchor = start
            )

        for body in joint_dict[end]:
            world.CreateRevoluteJoint(
                bodyA = body,
                bodyB = self.body,
                anchor = end
            )

        joint_dict[start].append(self.body)
        joint_dict[end].append(self.body)

        self.stress_color = (0, 255, 0)
        self.forces = 0# b2.vec2(0,0)

    def update(self):
        f_max = 3000
        c = min(self.forces, f_max)/f_max

        self.stress_color = (255*c, 255*(1-c), 0)
        self.forces = 0 #b2.vec2(0,0)


