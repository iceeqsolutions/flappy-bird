import pygame
from pygame.locals import *
import random

pygame.init()

# Game setup
clock = pygame.time.Clock()
fps = 60

# Game canvas variables
width = 800
height = 700
backgroundImg = pygame.image.load("background.jpg")
roadImg = pygame.image.load("road.jpg")
white = (255, 255, 255)
orange = (255, 202, 24)
font = pygame.font.SysFont('Snap ITC', 70)

# Game variables
startGame = False
gameOver = False
gameScore = 0
passedObstacle = False
roadImgScroll = 0
scrollSpeed = 5
addLogFrequency = 1000
previousLog = 0


# SPRITE CLASSES

# Create Game Text
def createText(text, font, color, x, y):
    displayText = font.render(text, True, color)
    screen.blit(displayText, (x, y))


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
        self.gravity = 0
        self.mouseKeyPressed = False

    def update(self):
        if startGame == True:            
            # handle the gravity
            if self.rect.bottom < 540:
                self.gravity += 0.5
                self.rect.y += self.gravity
            else:
                self.gravity = 10
            # print(self.gravity)

        if gameOver == False:
            # handle the wing movement
            self.counter += 1
            wingFlapPause = 5
            if self.counter > wingFlapPause:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

            # handle the increase in height
            if pygame.mouse.get_pressed()[0] == 1 and self.mouseKeyPressed == False:
                self.mouseKeyPressed = True
                if self.rect.top > 0:
                    self.gravity = -7
                else:
                    self.gravity = 0
            if pygame.mouse.get_pressed()[0] == 0 and self.mouseKeyPressed == True:
                self.mouseKeyPressed = False

            # handle bird wiggle during flight
            self.image = pygame.transform.rotate(self.images[self.index], self.gravity * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

flappyGroup = pygame.sprite.Group()
flappyBird = GameCharacter(150, int(height / 2))
flappyGroup.add(flappyBird)

# The wooden logs
class WoodenLog(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("woodenlog.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        # orientation 0 is top, 1 is bottom
        if orientation == 1:
            self.image = pygame.transform.flip(self.image, False, True) # flip on the x-axis = False, flip on the y-axis = True

    def update(self):
        if startGame == True:
            self.rect.x -= scrollSpeed
            if self.rect.right < 0:
                self.kill()

woodenLogGroup = pygame.sprite.Group()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Clone")

run = True
while run:
    clock.tick(fps)
    screen.blit(backgroundImg, (0, 0))

    flappyGroup.draw(screen)
    flappyGroup.update()
    woodenLogGroup.draw(screen)
    woodenLogGroup.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and startGame == False and gameOver == False:
            startGame = True
    
    # Check game score
    if len(woodenLogGroup) > 0:
        if flappyGroup.sprites()[0].rect.left > woodenLogGroup.sprites()[0].rect.left and flappyGroup.sprites()[0].rect.left < woodenLogGroup.sprites()[0].rect.right and passedObstacle == False:
            passedObstacle = True
        if flappyGroup.sprites()[0].rect.left > woodenLogGroup.sprites()[0].rect.right and passedObstacle == True:
            passedObstacle = False
            gameScore += 1
    # print(gameScore)
    createText(str(gameScore), font, white, width // 2, 50)

    # Check for Game Over
    if pygame.sprite.groupcollide(flappyGroup, woodenLogGroup, False, False):
        gameOver = True 
        # startGame = False # this will stop the game with the bird in mid-air, therefore removed
    if  flappyBird.rect.bottom >= 540:
        gameOver = True
        startGame = False
        createText('Game Over', font, orange, 200, 200)

    if startGame == True:
        currentTime = pygame.time.get_ticks()
        if currentTime > previousLog + addLogFrequency:
            previousLog = currentTime
            logPlacement = random.randint(-200, 0)
            woodenLogTop = WoodenLog(width, logPlacement, 0)
            woodenLogBottom = WoodenLog(width, logPlacement + 420, 1)
            woodenLogGroup.add(woodenLogTop)
            woodenLogGroup.add(woodenLogBottom)
         
    if abs(roadImgScroll) > 200:
        roadImgScroll = 0
    
    screen.blit(roadImg, (roadImgScroll, 530))
    if startGame == True:
        roadImgScroll -= scrollSpeed # pos moving from right to left

    pygame.display.flip()

pygame.quit()