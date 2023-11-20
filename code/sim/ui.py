import pygame
from enum import Enum
from Box2D.b2 import vec2

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

    def update(self, world):
        self.events = []

        keys = pygame.key.get_pressed()
        m1 = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2(mouse_pos[0], self.graphics.screen_size[1]-mouse_pos[1]) / self.graphics.PPM
        mouse_pos = vec2(round(mouse_pos[0]), round(mouse_pos[1]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.events.append(Event("quit"))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.events.append(Event("quit"))
                
                elif event.key == pygame.K_s:
                    self.events.append(Event("simulate"))

                elif event.key == pygame.K_r:
                    self.state = "remove"

                elif event.key == pygame.K_w:
                    self.state = "plank"

                elif event.key == pygame.K_e:
                    self.state = "road"
            
        if m1:
            if not self.clicked:
                self.clicked = True
                if self.state in ["plank", "road"]:
                    if self.click_start is None:
                        self.click_start = mouse_pos
                        
                    elif self.click_start is not None:
                        self.events.append(Event("add-"+self.state, data=(self.click_start, mouse_pos)))
                        self.click_start = None

                if self.state == "remove":
                    for body in world.bodies:
                        for fixtures in body.fixtures:
                            if fixtures.TestPoint(mouse_pos):
                                self.events.append(Event("remove", data=body))
                        

        else:
            self.clicked = False
