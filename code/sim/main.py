import pygame
from pygame.locals import QUIT
from Box2D import b2
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)


# Pygame setup
pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Box2D Joint Example")

PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

# Set up Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Box2D Joint Example")

def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, (128,128,128), vertices)
polygonShape.draw = my_draw_polygon


# Set up Box2D world
world = b2.world(gravity=(0, -10), doSleep=True)

# Create ground body
ground_body = world.CreateStaticBody(
    position=(0, -10),
    shapes=b2.polygonShape(box=(50, 10)),
)

size = b2.vec2(4,4)
fixture = b2.fixtureDef(shape=b2.polygonShape(box=size/2),
                        density=1,
                        friction=0.6)

# Create two dynamic bodies
box1 = world.CreateDynamicBody(position=(20, 20),
                               fixtures=fixture,
                               fixedRotation=False)

box2 = world.CreateDynamicBody(position=(17,17),
                               fixtures=fixture,
                               fixedRotation=False)

# Create a revolute joint between the two bodies
joint = world.CreateRevoluteJoint(
    bodyA=box1,
    bodyB=box2,
    anchor=box1.position-size/2,
    collideConnected=False,
)

# Set up Pygame clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Step Box2D simulation
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        world.Step(1.0/60, 6, 2)

    # Clear the screen
    screen.fill((0,0,0))

    # Draw ground
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)


    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()

