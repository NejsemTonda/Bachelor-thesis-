import Box2D
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody

def create_car(world, pos, speed=50):
    # Create the car body
    car_body = world.CreateDynamicBody(
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
            density=1
        ),
    )
    
    # Create the wheels
    circle_fixtureDef = Box2D.b2.fixtureDef(
        shape=circleShape(radius=0.4),
        density=1
    )

    wheel1 = world.CreateDynamicBody(
        position=car_body.position + (1, -1),
        fixtures=circle_fixtureDef,
            )
    
    wheel2 = world.CreateDynamicBody(
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

    return car_body, [wheel1, wheel2]
