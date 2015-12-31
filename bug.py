__author__ = 'Peter'
import time
import random
import pygame
import math
import Genome as genome
from vector import Vector as Vector
from colourConfig import Colours as Colours
from entityConfig import Entity

class BugGenerator():
    def __init__(self):
        pass

    def make_bug(self):
        someGenes = BugGenome()
        return Bug(1, someGenes)

class Bug(Entity):
    def __init__(self,id,genome):
        super(Bug, self).__init__()
        self.id = id
        self.genome = genome
        self.build()

    def action(self):
        if self.dead:
            return
        self.vector.dx += random.randint(-20,20)
        self.vector.dy += random.randint(-20,20)

    def clicked(self):
        self.die()

    def build(self):
        genes = self.genome.genes
        genome = self.genome.genes
        colourRaw = self.genome.get_trait("colour")
        if colourRaw == False:
            print("ERROR assigning colour to bug")
        colourRed = int(colourRaw[0:2],16)
        colourGreen = int(colourRaw[2:4],16)
        colourBlue = int(colourRaw[4:6],16)
        self.colour = [colourRed, colourGreen, colourBlue]

        size = self.genome.get_trait("size")
        if size == False:
            print("ERROR assigning size to bug")
        width = int(size[0:1],16)
        if width < 9:
            width = 9
        height = int(size[1:2],16)
        if height < 9:
            height = 9
        self.image = pygame.Surface((width,height))
        self.image.fill(Colours.White)
        self.size = [width, height]
        # print("Size: {}, Colour:{}".format(self.size, self.colour))
        self.set_reaction_speed(self.genome.get_trait("reactionSpeed"))

    def set_reaction_speed(self,speedRaw):
        if speedRaw != False:
            self.reactionSpeed = int(speedRaw,16)

    def input(self, dx, dy):
        if self.dead:
            return
        distance = math.sqrt( dx**2 + dy**2)
        angle = math.atan2(dy,dx)
        angleD = (angle*180)/math.pi
        # print("Bug ID: {} Angle cursor to mouse: {}".format(self.id, angleD))
        reactionSpeedMultiplier = self.reactionSpeed/255
        if distance < (50*reactionSpeedMultiplier):
            # print("angle:{}".format(angle))
            currentSpeed = math.sqrt(self.vector.dx**2 + self.vector.dy**2)
            maxSpeed = self.maxSpeed
            speedToAdd = maxSpeed - currentSpeed
            # topSpeed = 10 + 10*round((50-distance)/50)
            # 0 if distance = 50, 1 if distance = 0
            nextSpeed = currentSpeed + speedToAdd*abs((distance-50)/50)
            nextSpeed = nextSpeed * reactionSpeedMultiplier
            dx = -nextSpeed * math.cos(angle)
            dy = -nextSpeed * math.sin(angle)
            self.vector.dx = dx
            self.vector.dy = dy
            # cursor distance, angle -> dx dy
            # food distance, angle -> dx dy

    def render(self):
        colour = self.colour
        if not self.alive:
            colour = Colours.Black
        pygame.draw.ellipse(self.image, colour,(0, 0, self.size[0], self.size[1]), 0)
        pygame.draw.ellipse(self.image, Colours.Black,(0, 0, self.size[0], self.size[1]), 1)

    @property
    def surface(self):
        return self.image

class BugGenome:
    def __init__(self):
        self.genome = genome.Genome()
        self.genome.add_trait("colour",8)
        self.genome.add_trait("size",20)
        self.genome.add_trait("reactionSpeed",2)
        self.genome.add_trait("sprintSpeed",2)
        self.genome.add_trait("sprintDuration",2)

    @property
    def genes(self):
        return  self.genome.genes

if __name__ == "__main__":
    # bugGen = BugGenerator()
    # newBug = bugGen.make_bug()
    # rectan = newBug.image.get_rect(topleft=(100,100))
    # rectan[0] = 300
    # print("rect:{}".format(rectan))
    pass