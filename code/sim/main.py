import pygame
from pygame.locals import QUIT
from Box2D import b2
from Box2D.b2 import vec2 
import math

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


def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], screen_height - v[1]) for v in vertices]
    pygame.draw.polygon(screen, (128,128,128), vertices)

b2.polygonShape.draw = my_draw_polygon

def my_draw_edgeshape(edgeShape, body, fixture):
    vertices = [(body.transform * v) * PPM for v in edgeShape.vertices]
    vertices = [(v[0], screen_height - v[1]) for v in vertices]
    for v1, v2 in list(zip(vertices, vertices[1:])):
        pygame.draw.line(screen, (0, 255,0), v1,v2, 3)

b2.edgeShape.draw = my_draw_edgeshape

def draw_circle(pos, r=5, color=(255,0,0)):
    pos = pos*PPM
    pos = vec2(pos[0], screen_height-pos[1])
    pygame.draw.circle(screen, color, pos, r)

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


joint_dict = MyDict()
joint_dict[vec2(10, 10)] = [ground1]
joint_dict[vec2(30, 10)] = [ground2]



# Main game loop
mouse_pressed = False
plank_start, plank_end = None, None

def add_plank(word, joint_dict, start, end):
    mid = start + (end - start)/2
    a = mid-start
    angle = math.atan2(a[1], a[0])

    plank = world.CreateDynamicBody(
        position = mid,
        angle = angle,
        fixtures = b2.fixtureDef(shape = b2.polygonShape(box=((start-end).length/2, 0.25)),
                                density = 1,
                                friction = 0.6
        )
    ) 
    print(len(joint_dict))
    
    for body in joint_dict[start]:
        print("creating joint at start")
        world.CreateRevoluteJoint(
            bodyA = body,
            bodyB = plank,
            anchor = start
        )

    for body in joint_dict[end]:
        print("creating joint at end")
        world.CreateRevoluteJoint(
            bodyA = body,
            bodyB = plank,
            anchor = end
        )

    joint_dict[start].append(plank)
    joint_dict[end].append(plank)

    return plank
    

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
#    print(mouse_pos)

        

    if pygame.mouse.get_pressed()[0]:
        if not mouse_pressed:
            mouse_pressed = True
            if plank_start is None:
                plank_start = mouse_pos
            else:
                plank_end = mouse_pos
    else:
        mouse_pressed = False


    if plank_start and plank_end:
        fav = add_plank(world, joint_dict, plank_start, plank_end)  
        plank_start, plank_end = None, None

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        world.Step(1.0/60, 6, 2)

    # Clear the screen
    screen.fill((0,0,0))

    # Draw ground
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)

    draw_circle(mouse_pos)
    if plank_start:
        draw_circle(plank_start)
        mid = plank_start + (mouse_pos - plank_start)/2
        k = mid-plank_start
        a = math.atan2(k[1], k[0])
        draw_circle(mid)


    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()

