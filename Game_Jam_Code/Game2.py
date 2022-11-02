import sys
import math
import os
import pygame, sys
from pygame.locals import *
import random, time
import pygame

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Making colors, the numbers correspond to RGB values
BLACK = pygame.Color(0, 0, 0)         # Black
WHITE = pygame.Color(255, 255, 255)   # White
GREY = pygame.Color(128, 128, 128)   # Grey
RED = pygame.Color(255, 0, 0)       # Red 

 # create a surface on screen that has the size of 400 x 600
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)

# load and set the logo
logo = pygame.image.load(r"Logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Battle Royale")


#Make mouse crosshair
pygame.mouse.set_visible(False)
mousec = pygame.image.load("mouse_C.png").convert_alpha()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("King.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
             self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
             self.rect.move_ip(0,5)

         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def look(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(mousec, (mouse_x, mouse_y))
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        rect = self.image.get_rect(center=self.rect.center)   
        screen.blit(self.newimage,rect)
        pygame.display.update()


P1 = Player()

while True:
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == event.type == MOUSEBUTTONDOWN and event.button == 1:
                print("test1")
            elif event.type == event.type == MOUSEBUTTONDOWN and event.button == 3:
                print("test3")
    
    P1.move()
    screen.fill(WHITE)
    P1.look()
    


    
    
              

    pygame.display.update()
    FramePerSec.tick(FPS) 