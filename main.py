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

    def update(self):
        self.counter += 1
        flapCD = 5

        if self.counter > flapCD:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images): 
                self.index = 0
        self.image = self.images[self.index]

birdGroup = pygame.sprite.Group()

flappy = Bird(100, int(screenHeight/2))

birdGroup.add(flappy)

run = True
while run:
    clock.tick(fps) # Sets game to 60fps

    screen.blit(bg, (0,0)) # Draw background

    birdGroup.draw(screen)
    birdGroup.update()
    
    screen.blit(ground, (groundScroll, 768)) # Draw and scroll ground
    groundScroll -= scrollSpeed
    if abs(groundScroll) > 35:
        groundScroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    pygame.display.update()

pygame.quit()