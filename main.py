import pygame
from pygame.locals import *

pygame.init()

# Game canvas variables
width = 800
height = 600
backgroundImg = pygame.image.load("background.jpg")

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Clone")

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.blit(backgroundImg, (0, 0))
    pygame.display.flip()

pygame.quit()