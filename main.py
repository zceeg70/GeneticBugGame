__author__ = 'Peter'

import time
import random
import pygame
import math
import Genome as genome

HEIGHT,WIDTH = 600,800
SCREEN = WIDTH, HEIGHT
class Colours:
    White = [255,255,255]
    Red = [255,0,0]
    Green = [0,255,0]
    Blue = [0,0,255]
    Black = [0,0,0]

class Config:
    MUTATE_CHANCE = 2/100

class GeneCategories:
    Size = True
    Speed = True
    Colour = True
    Energy = False

class Instruction:
    def __init__(self,cost,callback):
        self.callback = callback
        self.cost = cost

class Vector:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.x = 300
        self.y = 400

class Bug(pygame.sprite.Sprite):
    def __init__(self,id,genome):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4,4))
        self.image.fill(Colours.White)
        # self.rect = self.image.get_rect()
        self.instructionList = []
        self.maxInstructions = 10
        self.maxSpeed = 60
        self.dead = False
        self.id = id
        self.genome = genome
        self.vector = Vector()

    def action(self):
        if self.dead:
            return
        self.vector.dx += random.randint(-20,20)
        self.vector.dy += random.randint(-20,20)
        # print("Bug changing direction")

    def clicked(self):
        self.dead = True
        self.dx = 0
        self.dy = 0

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
    @property
    def rect(self):
        return self.image.get_rect(topleft=(self.vector.x,self.vector.y))

    def get_surface(self):
        colour = self.colour
        if self.dead:
            colour = Colours.Black
        # pygame.draw.circle(self.image,colour,self.size,5,0)
        pygame.draw.ellipse(self.image, colour,(0, 0, self.size[0], self.size[1]), 0)
        pygame.draw.ellipse(self.image, Colours.Black,(0, 0, self.size[0], self.size[1]), 1)

class BugGenome:
    def __init__(self):
        self.genome = genome.Genome()
        self.genome.add_trait("colour",8)
        self.genome.add_trait("size",20)
        self.genome.add_trait("reactionSpeed",2)
        self.genome.add_trait("sprintSpeed",2)
        self.genome.add_trait("sprintDuration",2)

class Population:
    def __init__(self):
        self.bugList = []
        self.spriteGroup = pygame.sprite.Group()


    def spawn(self, bugs = 22):
        for x in range(1,bugs):
            newBugGenes = BugGenome()
            newBug = Bug(x,newBugGenes.genome)
            newBug.vector.x = random.randint(round(WIDTH*0.10),round(WIDTH*0.90))
            newBug.vector.y = random.randint(round(HEIGHT*0.10),round(HEIGHT*0.90))
            newBug.build()
            self.spriteGroup.add(newBug)
            self.bugList.append(newBug)

    # for rendering
    def get_positions_and_surfaces(self):
        surfaceList = []
        for bug in self.bugList:
            position = [round(bug.vector.x),round(bug.vector.y)]
            surface = bug.get_surface()
            surfaceList.append([position,bug])
        return self.spriteGroup

    def input(self,value):
        # print("value:{}".format(value))
        x = value[0]
        y = value[1]
        for bug in self.bugList:
            dx = x - round(bug.vector.x)
            dy = y - round(bug.vector.y)
            # print("dx:{},dy:{}".format(dx,dy))
            bug.input(dx,dy)

    def action(self):
        for bug in self.bugList:
            bug.action()

    def breed(self):
        pass

    def mutate(self):
        pass

# BUG = Bug()
def start_program_loop():
    pygame.init()
    # BUG.vector.dx = 40
    # BUG.vector.dy = 10
    run_program()

def run_program():
    running = True
    drawPeriod = 1.0/60
    logicPeriod = 1.0/100
    population = Population()
    population.spawn()

    mainScreen = pygame.display.set_mode(SCREEN)
    mainScreen.fill(Colours.White)
    nextLogic = time.time()
    nextRender = time.time()
    nextSecond = time.time() + 4
    while running:
        # pygame.time.delay(900)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                clicked = [s for s in population.bugList if s.rect.collidepoint(mousePos)]
                for bug in clicked:
                    bug.clicked()
                    population.bugList.remove(bug)

        if time.time() > nextLogic:
            nextLogic += logicPeriod
            mousePos = pygame.mouse.get_pos()

            population.input(mousePos)
            for bug in population.bugList:
                if bug.dead:
                    continue
                if (bug.vector.x + bug.vector.dx*logicPeriod) > WIDTH:
                    bug.vector.dx = -bug.vector.dx
                elif (bug.vector.x + bug.vector.dx*logicPeriod) < 0:
                    bug.vector.dx = -bug.vector.dx
                if (bug.vector.y + bug.vector.dy)> HEIGHT:
                    bug.vector.dy = -bug.vector.dy
                elif (bug.vector.y + bug.vector.dy*logicPeriod) < 0:
                    bug.vector.dy = -bug.vector.dy
                bug.vector.x += bug.vector.dx*logicPeriod
                bug.vector.y += bug.vector.dy*logicPeriod
            if len(population.bugList)<5:
                mainScreen.fill(Colours.Green)



        if time.time() > nextSecond:
            nextSecond = time.time() + 1
            population.action()


        if time.time() >= nextRender:
            nextRender = time.time() + drawPeriod
            mainScreen.fill(Colours.White)
            sprites = population.get_positions_and_surfaces()
            sprites.draw(mainScreen)
            pygame.display.flip()



def main():
    # print("hello world {}".format(time.time()))
    start_program_loop()
    pygame.quit()
if __name__ == "__main__":
    try:
        main()
    except:
        pygame.quit()
        raise