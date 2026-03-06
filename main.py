import pygame
from pygame.locals import *
import random

pygame.init()

screenWidth = 864
screenHeight = 936

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("67-FlappyBird")

# Load assets
bg = pygame.image.load("assets/bg.png")
ground = pygame.image.load("assets/ground.png")
restart = pygame.image.load("assets/restart.png")

font_45 = pygame.font.Font("assets/PixelOperator8.ttf", 45)
font_20 = pygame.font.Font("assets/PixelOperator8.ttf", 20)
white = (255, 255, 255)
black = (0, 0, 0)

# Game variables
groundScroll = 0
scrollSpeed = 4
gameStart = False
gameOver = False
pipeGap = 200
pipeFreq = 1500 #1500ms == 1.5s
lastPipe = pygame.time.get_ticks() - pipeFreq
score = 0
passPipe = False


clock = pygame.time.Clock()
fps = 60

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4): # Append sprite frames to images
            img = pygame.image.load(f"assets/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if gameStart == True:
            self.vel += 0.5 # Bird gravity
            if self.vel > 8:
                self.vel = 8 # Terminal velocity
            if self.rect.bottom < 768:
                self.rect.y +=(self.vel)

        if gameOver == False:
            self.counter += 1 # Flap animation
            flapCD = 5

            if self.counter > flapCD:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images): 
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], -self.vel * 3) # Rotate bird based on velocity
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90) # Dead bird (Rotate bird to face down)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/pipe.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

        if position == 1: # Top pipe
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipeGap / 2)]
        if position == -1: # Bottom pipe
            self.rect.topleft = [x, y + int(pipeGap / 2)]
    
    def update(self):
        self.rect.x -= scrollSpeed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        pygame.transform.scale_by(self.image, 2)
    
    def draw(self):
        action = False

        pos = pygame.mouse.get_pos() # Check mouse position

        if self.rect.collidepoint(pos): # Check if mouse is over the button
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

def drawText(text, font, color, x, y, align="topLeft"): # Function for drawing text on the screen
    img = font.render(text, True, color)
    rect = img.get_rect()

    if align == "center": # Align text to the center
        rect.center = (x, y)
    elif align == "midTop": # Align text to the middle top
        rect.midtop = (x, y)
    elif align == "midBottom": # Align text to the middle bottom
        rect.midbottom = (x, y)
    else:  # default: topLeft
        rect.topleft = (x, y)

    screen.blit(img, rect)

def restartGame(): # Function for resetting game variables and sprites
    pipeGroup.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screenHeight / 2)
    score = 0

    drawText("Press Space to Start", font_20, black, screenWidth / 2 , screenHeight / 2, "center")

    return score


birdGroup = pygame.sprite.Group()
pipeGroup = pygame.sprite.Group()

flappy = Bird(100, int(screenHeight / 2))

birdGroup.add(flappy)

restartButton = Button(screenWidth / 2 - 50, screenHeight / 2 + 100, restart)

run = True
while run:
    clock.tick(fps) # Sets game to 60fps

    screen.blit(bg, (0,0)) # Draw background

    birdGroup.draw(screen)
    birdGroup.update()
    pipeGroup.draw(screen)

    screen.blit(ground, (groundScroll, 768)) # Draw ground

    if len(pipeGroup) > 0:
        if birdGroup.sprites()[0].rect.left > pipeGroup.sprites()[0].rect.left and birdGroup.sprites()[0].rect.right < pipeGroup.sprites()[0].rect.right and passPipe == False: # Check if bird is inbetween the two vertical pipes
            passPipe = True
        if passPipe == True:
            if birdGroup.sprites()[0].rect.left > pipeGroup.sprites()[0].rect.right: # Check if the bird has left the zone in between the two vertical pipes
                passPipe = False
                score += 1
    
    drawText("Score: " + str(score), font_45, white, 10, 20, "topLeft") # Display score

    if gameStart == False and gameOver == False:
        drawText("Press Space to Start", font_20, black, screenWidth / 2 , screenHeight / 2, "center")

    if pygame.sprite.groupcollide(birdGroup, pipeGroup, False, False) or flappy.rect.top < 0:
        gameOver = True

    if flappy.rect.bottom >= 768: # Check if bird hits the ground
        gameOver = True
        gameStart = False
        flappy.vel = 0
        flappy.rect.bottom = 768
        print("Game Over")

    if gameOver == False and gameStart == True:
        timeNow = pygame.time.get_ticks()
        if timeNow - lastPipe > pipeFreq: # Generate pipes
            pipeHeight = random.randint(-125, 125) # Generate height of pipe

            bottomPipe = Pipe(screenWidth, int(screenHeight / 2) + pipeHeight, -1)
            topPipe = Pipe(screenWidth, int(screenHeight / 2) + pipeHeight, 1)
            pipeGroup.add(topPipe)
            pipeGroup.add(bottomPipe)
            lastPipe = timeNow
        
        pipeGroup.update()

        groundScroll -= scrollSpeed # Scroll ground
        if abs(groundScroll) > 35:
            groundScroll = 0

    if gameOver == True:
        if restartButton.draw() == True:
            gameOver = False
            score = restartGame() # Reset game and score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN: # Check for spacebar press
            if event.key == pygame.K_SPACE and gameOver == False:
                if gameStart == False: # If game has not started, start the game
                    gameStart = True
                    flappy.clicked = True
                    flappy.vel = -10
                    print("Game Started")
                else: # If game has already started, flap the bird
                    flappy.clicked = True 
                    flappy.vel = -10
                    print("Flap")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                flappy.clicked = False

        
    pygame.display.update()

pygame.quit()