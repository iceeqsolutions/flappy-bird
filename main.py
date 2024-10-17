import pygame
from pygame.locals import *

pygame.init()

# Game setup
clock = pygame.time.Clock()
fps = 60

# Game canvas variables
width = 800
height = 700
backgroundImg = pygame.image.load("background.jpg")
roadImg = pygame.image.load("road.jpg")

# Game variables
roadImgScroll = 0
scrollSpeed = 5

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Clone")

run = True
while run:
    clock.tick(fps)
    screen.blit(backgroundImg, (0, 0))
    screen.blit(roadImg, (roadImgScroll, 530))
    roadImgScroll -= scrollSpeed # pos moving from right to left
    if abs(roadImgScroll) > 200:
        roadImgScroll = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()