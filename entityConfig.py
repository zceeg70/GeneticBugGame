__author__ = 'Peter'
import pygame
from vector import Vector

# base class to build game pygame creatures on. sets up the pygame surface, with a vector.
# bounds defines the game area to keep the sprite within, checked within the update methods
# the inheriting class should draw to the
class Entity(pygame.sprite.Sprite):
    def __init__(self, bounds=[0,600,0,800], size=(4,4)):
        pygame.sprite.Sprite.__init__(self)
        self.update_surface_size(size) #creates scope variable "image", which is a pygame surface
        self.alive = True
        self.bounds = bounds
        self.vector = Vector()

    def die(self):
        self.alive = False
        self.vector.dx = 0
        self.vector.dy = 0

    def update(self, timestep = 1):
        self.update_position(timestep)

    def update_position(self, timestep = 1):
        self.vector.update(timestep)

    def update_surface_size(self, size=(1,1)):
        self.image = pygame.Surface(size)


    def set_size(self, size=(1,1)):
        self.update_surface_size(size)

    @property
    def orientation(self):
        return self.vector.orientation()

    @property
    def rect(self):
        return self.image.get_rect(topleft=(self.vector.x,self.vector.y))