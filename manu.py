import pygame
from pygame.locals import *

def init():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Turning circle')
    clock = pygame.time.Clock()

def loop():
    while 1:
        clock.tick(25)
        pygame.display.flip()
        for event in pygame.event.get():

            if event.type == QUIT:
                exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    exit(0)

init()
loop()
