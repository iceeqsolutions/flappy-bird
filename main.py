import pygame
from pygame.locals import *

pygame.init()

# Game canvas variables
width = 800
height = 700
backgroundImg = pygame.image.load("background.jpg")
roadImg = pygame.image.load("road.jpg")

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Clone")

run = True
while run:
    screen.blit(backgroundImg, (0, 0))
    screen.blit(roadImg, (0, 530))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()