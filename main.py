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

# SPRITE CLASSES
# The Bird
class GameCharacter(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self) # allows to iherit from the sprite class
        self.images = []
        self.index = 0
        self.counter = 0 # controls the speed of the animation
        for num in range(1, 5):
            img = pygame.image.load(f"bird{num}sm.png")
            self.images.append(img)
            # print(f"bird{num}sm.png")
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        # handle the animation
        self.counter += 1
        wingFlapPause = 5
        if self.counter > wingFlapPause:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

flappyGroup = pygame.sprite.Group()
flappyBird = GameCharacter(150, int(height / 2))
flappyGroup.add(flappyBird)

# The wooden logs
class WoodenLog(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("woodenlog.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

woodenLogGroup = pygame.sprite.Group()
woodenLogTop = WoodenLog(300, 0)
woodenLogBottom = WoodenLog(300, height - 360)
woodenLogGroup.add(woodenLogTop)
woodenLogGroup.add(woodenLogBottom)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Clone")

run = True
while run:
    clock.tick(fps)
    screen.blit(backgroundImg, (0, 0))
    screen.blit(roadImg, (roadImgScroll, 530))
    roadImgScroll -= scrollSpeed # pos moving from right to left
    flappyGroup.draw(screen)
    flappyGroup.update()
    woodenLogGroup.draw(screen)
    woodenLogGroup.update()
    if abs(roadImgScroll) > 200:
        roadImgScroll = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()