import pygame
from pygame.locals import *
import random

class Player:
    def __init__(self):
        self.x = 32*4
        self.y = 32*4

def init():
    global screen, clock, maze, shipPoly, player
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Turning circle')
    clock = pygame.time.Clock()
    maze = [0]*64
    for i in range(0,64): maze[i] = [0]*64
    random.seed(2013)
    createMaze(maze)
    shipPoly = [ (0,2), (2,-2), (0,-1), (-2,-2), (0,2) ]
    shipPoly = polyScale(shipPoly, 32)
    player = Player()

def createMaze(maze):
    for x in range(0,64):
        for y in range(0,64):
            maze[x][y] = random.choice([0,1])

def polyScale(poly,scale):
    newPoly = []
    for p in poly:
        newPoly.append((p[0]*scale, p[1]*scale))
    return newPoly

def polyTranslate(poly,x,y):
    newPoly = []
    for p in poly:
        newPoly.append((p[0]+x, p[1]+y))
    return newPoly

def loop():
    while 1:
        clock.tick(25)
        pygame.display.flip()
        for event in pygame.event.get():
            for x in range(0,64):
                for y in range(0,64):
                    if(maze[x][y] == 1):
                        pygame.draw.rect(screen, (255,255,255), (x*64,y*64,64,64))
            shipTransPoly = polyTranslate(shipPoly,player.x,player.y)
            pygame.draw.polygon(screen, (255,0,0), shipTransPoly)
            if event.type == QUIT:
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    exit(0)

init()
loop()
