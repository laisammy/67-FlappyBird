import pygame
from pygame.locals import *

pygame.init()

screenWidth = 864
screenHeight = 936

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("67-FlappyBird")

# Load assets
bg = pygame.image.load("assets/bg.png")
ground = pygame.image.load("assets/ground.png")

# Game variables
groundScroll = 0
scrollSpeed = 4
gameStart = False
gameOver = False

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


birdGroup = pygame.sprite.Group()

flappy = Bird(100, int(screenHeight/2))

birdGroup.add(flappy)

run = True
while run:
    clock.tick(fps) # Sets game to 60fps

    screen.blit(bg, (0,0)) # Draw background

    birdGroup.draw(screen)
    birdGroup.update()

    screen.blit(ground, (groundScroll, 768)) # Draw ground

    if flappy.rect.bottom >= 768: # Check if bird hits the ground
        gameOver = True
        gameStart = False
        flappy.vel = 0
        flappy.rect.bottom = 768
        print("Game Over")

    if gameOver == False:
        groundScroll -= scrollSpeed # Scroll ground
        if abs(groundScroll) > 35:
            groundScroll = 0

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