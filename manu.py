import pygame
from pygame.locals import *
import random

def init():
    global screen, clock, maze
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Turning circle')
    clock = pygame.time.Clock()
    maze = [0]*64
    for i in range(0,64): maze[i] = [0]*64
    random.seed(2013)
    createMaze(maze)
def createMaze(maze):
    for x in range(0,64):
        for y in range(0,64):
            maze[x][y] = random.choice([0,1])

def loop():
    while 1:
        clock.tick(25)
        pygame.display.flip()
        for event in pygame.event.get():
            for x in range(0,64):
                for y in range(0,64):
                    if(maze[x][y] == 1):
                        pygame.draw.rect(screen, (255,255,255), (x*64,y*64,64,64))
            if event.type == QUIT:
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    exit(0)

init()
loop()
