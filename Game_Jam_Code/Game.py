import sys
import os
import pygame, sys
from pygame.locals import *
import random
os.path.join(r"GameJam2022", r"Images")
# import the pygame module, so you can use it
import pygame
 

    # initialize the pygame module
pygame.init()
    # load and set the logo
logo = pygame.image.load(r"Logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Battle Royale")

    # Making colors, the numbers correspond to RGB values
BLACK = pygame.Color(0, 0, 0)         # Black
WHITE = pygame.Color(255, 255, 255)   # White
GREY = pygame.Color(128, 128, 128)   # Grey
RED = pygame.Color(255, 0, 0)       # Red 

    # create a surface on screen that has the size of 300 x 300
screen = pygame.display.set_mode((400,600))
screen.fill(WHITE)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 
 
      def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
 
      def draw(self, surface):
        surface.blit(self.image, self.rect) 
    # Make a movable character
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("King.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
 
    def update(self):
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

P1 = Player()
E1 = Enemy()

FPS = 60
FramePerSec = pygame.time.Clock()
     
    # This is the while loop that keeps the game running, every time that an event happens, this loop checks if that event was quitting. If it was, the game quits. 
while True:
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
    P1.update()
    E1.move()
     
    screen.fill(WHITE)
    P1.draw(screen)
    E1.draw(screen)
         
    pygame.display.update()
    FramePerSec.tick(FPS) 
    