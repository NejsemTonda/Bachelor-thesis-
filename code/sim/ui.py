import pygame
from enum import Enum
from Box2D.b2 import vec2
from helpers import correctLen

class Event():
	def __init__(self, type, data=None):
		self.type = type
		if data is not None:
			self.data = data

class UI():
	def __init__(self, graphics):
		self.graphics = graphics
		self.state = "plank"
		self.click_start = None
		self.clicked = False
		self.events = []
		self.mouse_pos = vec2(0,0)
		self.max_plank_len = 10

	def update(self, world):
		self.events = []

		keys = pygame.key.get_pressed()
		m1 = pygame.mouse.get_pressed()[0]
		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_pos = vec2(self.mouse_pos[0], self.graphics.screen_size[1]-self.mouse_pos[1]) / self.graphics.PPM
		self.mouse_pos = vec2(round(self.mouse_pos[0]), round(self.mouse_pos[1]))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.events.append(Event("quit"))

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.events.append(Event("quit"))
				
				elif event.key == pygame.K_s:
					self.events.append(Event("sim"))

				elif event.key == pygame.K_d:
					self.state = "remove"

				elif event.key == pygame.K_p:
					self.state = "plank"

				elif event.key == pygame.K_r:
					self.state = "road"
			
		if m1:
			if not self.clicked:
				self.clicked = True
				if self.state in ["plank", "road"]:
					if self.click_start is None:
						self.click_start = self.mouse_pos
						
					elif self.click_start is not None:
						self.events.append(Event("add-"+self.state, data=(self.click_start, self.mouse_pos)))
						self.click_start = None

				if self.state == "remove":
					for body in world.bodies:
						for fixtures in body.fixtures:
							if fixtures.TestPoint(self.mouse_pos):
								self.events.append(Event("remove", data=body))
						

		else:
			self.clicked = False

	def draw(self):
		self.graphics.draw_circle(self.mouse_pos, r=0.2)
		if self.click_start is not None:
			self.graphics.draw_circle(self.click_start, r=0.2)
			end = correctLen(self.click_start, self.mouse_pos, self.max_plank_len)
			self.graphics.draw_line(self.click_start, end)
