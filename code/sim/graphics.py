from Box2D.b2 import vec2
import pygame        

class Graphics:
    def __init__(self, PPM=20, size=vec2(800,600), fps=60):

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_size = size
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Poly Bridge in Box2D Example")
        self.fps = fps

    def clear(self, background=(0,0,0)):
        self.screen.fill(background)

    def draw(self):
        pygame.display.flip()
        self.clock(self.fps)

    def draw_circle(self, pos, r=5, color=(255,0,0)):
        pos = pos*self.PPM
        pos = vec2(pos.x, self.screen_size.y-pos.y)
        pygame.draw.circle(self.screen, color, pos, r)


    def draw_polygon(self, polygon, color=(128, 128, 128)):
        for shape in [f.shape for f in polygon.fixtures]:
            vertices = [(polygon.transform * v) * self.PPM for v in shape.vertices]
            vertices = [(v[0], self.screen_size.y - v[1]) for v in vertices]
            pygame.draw.polygon(self.screen, color, vertices)

    def draw_edgeshape(self, edgeShape, color = (0,255,0)):
        for shape in [f.shape for f in edgeShape.fixtures]:
            vertices = [(edgeShape.transform * v) * self.PPM for v in shape.vertices]
            vertices = [(v[0], self.screen_size.y - v[1]) for v in vertices]
            for v1, v2 in list(zip(vertices, vertices[1:])):
                pygame.draw.line(self.screen, color, v1,v2, 3)



        
