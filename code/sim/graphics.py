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
		self.PPM = PPM

	def clear(self, background=(0,0,0)):
		self.screen.fill(background)

	def draw(self):
		pygame.display.flip()
		self.clock.tick(self.fps)

	def draw_circle(self, pos, r=0.25, color=(255,0,0), hollow=False):
		pos = pos*self.PPM
		pos = vec2(pos.x, self.screen_size.y-pos.y)
		if hollow:
			pygame.draw.circle(self.screen, color, pos, r*self.PPM, width=2)
		else:
			pygame.draw.circle(self.screen, color, pos, r*self.PPM)
			


	def draw_polygon(self, polygon, color=(128, 128, 128)):
		for shape in [f.shape for f in polygon.fixtures]:
			vertices = [(polygon.transform * v) * self.PPM for v in shape.vertices]
			vertices = [(v[0], self.screen_size.y - v[1]) for v in vertices]
			pygame.draw.polygon(self.screen, color, vertices)

	def draw_line(self, start, end, color=(0,255,0), t=0.1):
		p1 = start * self.PPM
		p1 = vec2(p1.x, self.screen_size.y - p1.y)
		p2 = end * self.PPM
		p2 = vec2(p2.x, self.screen_size.y - p2.y)

		pygame.draw.line(self.screen, color, p1, p2, int(t*self.PPM))

	def draw_edgeshape(self, edgeShape, color = (0,255,0)):
		for shape in [f.shape for f in edgeShape.fixtures]:
			vertices = [(edgeShape.transform * v) * self.PPM for v in shape.vertices]
			vertices = [(v[0], self.screen_size.y - v[1]) for v in vertices]
			for v1, v2 in list(zip(vertices, vertices[1:])):
				pygame.draw.line(self.screen, color, v1,v2, 3)



		
