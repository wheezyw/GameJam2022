import sys
import math
import os
import pygame, sys
from pygame.locals import *
import random, time
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
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)




    # Make a movable character
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
             pygame.transform.rotate(self.image, 180)
             pygame.display.flip
        if pressed_keys[K_DOWN]:
             self.rect.move_ip(0,5)
             pygame.transform.rotate(self.image, 180)
             pygame.display.flip
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
                  pygame.transform.rotate(self.image, 180)
                  pygame.display.flip
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  pygame.transform.rotate(self.image, 180)
                  pygame.display.flip

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, Player):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.player = Player 
        self.player.rect = self.player.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),random.randint(40, SCREEN_HEIGHT-40)) 



 
    def move(self):
        # Find direction vector (dx, dy) between enemy and player.
        

        dirvect = pygame.math.Vector2(self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)
        if (dirvect.x > 0 or dirvect.y > 0):
            dirvect.normalize()
            # Move along this normalized vector towards the player at current speed.
            self.speed = 5
            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)
        if (dirvect.x == 0 and dirvect.y == 0):
            pygame.locals.QUIT()
            sys.exit()
    def draw(self, surface):
        surface.blit(self.image, self.rect) 

#Setting up Sprites
P1 = Player()
E1 = Enemy(P1)
E2 = Enemy(P1)

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1, E2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, E2)

FPS = 60
FramePerSec = pygame.time.Clock()
     
    # This is the while loop that keeps the game running, every time that an event happens, this loop checks if that event was quitting. If it was, the game quits. 
while True:
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
    P1.move()
    E1.move(P1)
    E2.move(P1)
    
     
    screen.fill(WHITE)
    P1.draw(screen)
    E1.draw(screen)
    E2.draw(screen)
              
    #Moves and Re-draws all sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
            screen.fill(RED)
            pygame.display.update()
            for entity in all_sprites:
                entity.kill()
            time.sleep(2)
            pygame.quit()
            sys.exit()



    pygame.display.update()
    FramePerSec.tick(FPS) 
    