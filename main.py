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

clock = pygame.time.Clock
fps = 60


run = True
while run:
    clock.tick(fps) # Sets game to 60fps

    screen.blit(bg, (0,0)) # Draw background
    
    screen.blit(ground, (groundScroll, 768)) # Draw and scroll ground
    groundScroll -= scrollSpeed
    if abs(groundScroll) > 35:
        groundScroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    pygame.display.update()

pygame.quit()