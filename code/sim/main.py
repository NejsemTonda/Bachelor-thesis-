import pygame
from pygame.locals import QUIT
from Box2D import b2
from Box2D.b2 import vec2 
import math
from graphics import Graphics
from plank import Plank

class MyDict(dict):
    def __init__(self, d = {}):
        self.dict = d

    def __getitem__(self, key):
        h = hash((key.x, key.y))
        if h not in self.dict:
            self.dict[h] = []
        return self.dict[h]

    def __setitem__(self, key, value):
        h = hash((key.x, key.y))
        self.dict[h] = value
        


# Pygame setup
pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 800, 600
PPM = 20.0  # pixels per meter
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Box2D Joint Example")

graphics = Graphics(screen, 20, vec2(screen_width, screen_height))
joint_dict = MyDict()



# Set up Box2D world
world = b2.world(gravity=(0, -10), doSleep=True)

# Create ground body
ground1 = world.CreateBody()
ground1.CreateEdgeChain(
    [(0,10), (10,10), (10,0)]
)

ground2 = world.CreateBody()
ground2.CreateEdgeChain(
    [(40,10), (30,10), (30,0)]
)


size = b2.vec2(4,4)
fixture = b2.fixtureDef(shape=b2.polygonShape(box=size/2),
                        density=1,
                        friction=0.6)

box1 = world.CreateDynamicBody(position=(20, 20),
                               fixtures=fixture,
                               fixedRotation=False)




# Create two dynamic bodies
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


joint_dict[vec2(10, 10)] = [ground1]
joint_dict[vec2(30, 10)] = [ground2]


planks = []

# Main game loop
mouse_pressed = False
plank_start, plank_end = None, None

running = True
fav = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Step Box2D simulation
    mouse_pos = vec2(pygame.mouse.get_pos())
    mouse_pos[1] = screen_height - mouse_pos[1] 
    mouse_pos = mouse_pos/PPM
    mouse_pos = vec2(round(mouse_pos[0]), round(mouse_pos[1]))

        

    if pygame.mouse.get_pressed()[0]:
        if not mouse_pressed:
            mouse_pressed = True
            if plank_start is None:
                plank_start = mouse_pos
            else:
                plank_end = mouse_pos
    else:
        mouse_pressed = False

    if fav:
        print(fav.GetReactionForce(60).length)
        print(fav.GetReactionTorque(60))

    if plank_start and plank_end:
        plank = Plank(world, joint_dict, plank_start, plank_end)  
        planks.append(plank)
        plank_start, plank_end = None, None

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        world.Step(1.0/60, 6, 2)


    for j in world.joints:
        f = j.GetReactionForce(60)
        for p in planks:
            if p.body == j.bodyA or p.body == j.bodyB:
                p.forces += f


    # Clear the screen
    screen.fill((0,0,0))
    graphics.draw_edgeshape(ground1)
    graphics.draw_edgeshape(ground2)

    graphics.draw_polygon(box1)
    graphics.draw_polygon(box2)

    for p in planks:
        p.update()
        graphics.draw_polygon(p.body, color=p.stress_color)

    graphics.draw_circle(mouse_pos)
    if plank_start:
        graphics.draw_circle(plank_start)
        mid = plank_start + (mouse_pos - plank_start)/2
        k = mid-plank_start
        a = math.atan2(k[1], k[0])
        graphics.draw_circle(mid)


    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()

