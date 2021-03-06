__author__ = 'Peter'

import time
import random
import pygame
import math
import Genome as genome
from bug import Bug
from bug import BugGenome
from colourConfig import Colours as Colours
from viewFSM import CurrentState as ViewController

HEIGHT,WIDTH = 600,800
SCREEN = WIDTH, HEIGHT


class Population:
    def __init__(self):
        self.bugList = []
        # self.spriteGroup = pygame.sprite.Group()
        self.genomeList = []

    def spawn_bugs(self, bugs = 22):
        for count in range(0,bugs):
            newGenome = BugGenome()
            self.genomeList.append(newGenome.genome)
        self.build_bugs()

    def build_bugs(self):
        for count in range(0,len(self.genomeList)):
            newBug = Bug(count, self.genomeList.pop())
            self.bugList.append(newBug)

    # def spawn(self, bugs = 22):
    #     for x in range(1,bugs):
    #         newBugGenes = BugGenome()
    #         newBug = Bug(x,newBugGenes.genome)
    #         newBug.vector.x = random.randint(round(WIDTH*0.10),round(WIDTH*0.90))
    #         newBug.vector.y = random.randint(round(HEIGHT*0.10),round(HEIGHT*0.90))
    #         newBug.build()
    #         self.spriteGroup.add(newBug)
    #         self.bugList.append(newBug)

    # for rendering
    # def get_positions_and_surfaces(self):
    #     surfaceList = []
    #     for bug in self.bugList:
    #         position = [round(bug.vector.x),round(bug.vector.y)]
    #         surface = bug.get_surface()
    #         surfaceList.append([position,bug])
    #     return self.spriteGroup

    # def input(self,value):
    #     # print("value:{}".format(value))
    #     x = value[0]
    #     y = value[1]
    #     for bug in self.bugList:
    #         dx = x - round(bug.vector.x)
    #         dy = y - round(bug.vector.y)
    #         # print("dx:{},dy:{}".format(dx,dy))
    #         bug.input(dx,dy)

    # def action(self):
    #     for bug in self.bugList:
    #         bug.action()

class Rendering:
    __instance = None
    def __init__(self):
        if Rendering.__instance is None:
            __instance = True
        else:
            return
        self.gameScreen = pygame.display.set_mode(SCREEN)
        self.entityList = pygame.sprite.Group()

    def update_game_screen(self, timestep = 1):
        self.gameScreen.fill(Colours.White) # replace with map
        self.entityList.draw(self.gameScreen)
        # sprites.draw(mainScreen)

    def flip_screen(self):
       pygame.display.flip()

    def set_entity_list(self, listToSet):
        for entity in listToSet:
            # check for quality
            self.entityList.add(entity)

def start_program_loop():
    pygame.init()
    # BUG.vector.dx = 40
    # BUG.vector.dy = 10
    run_program()

def run_program():
    running = True
    drawPeriod = 1.0/60
    logicPeriod = 1.0/100
    bugPopulation = Population()
    bugPopulation.spawn_bugs(25)

    # mainScreen = pygame.display.set_mode(SCREEN)
    # mainScreen.fill(Colours.White)
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
                clicked = [s for s in bugPopulation.bugList if s.rect.collidepoint(mousePos)]
                for bug in clicked:
                    bug.clicked()
                    bugPopulation.bugList.remove(bug)

        if time.time() > nextLogic:
            nextLogic += logicPeriod
            mousePos = pygame.mouse.get_pos()

            # population.input(mousePos)
            bugPopulation.update()
            for bug in bugPopulation.bugList:
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
            # if len(bugPopulation.bugList)<5:
            #     mainScreen.fill(Colours.Green)

        # if time.time() > nextSecond:
        #     nextSecond = time.time() + 1
        #     population.action()


        if time.time() >= nextRender:
            nextRender = time.time() + drawPeriod
            ViewController.refresh()
            # Rendering.update_game_screen()
            # mainScreen.fill(Colours.White)
            # sprites = population.get_positions_and_surfaces()
            # sprites.draw(mainScreen)
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