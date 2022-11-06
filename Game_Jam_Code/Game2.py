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
punch_time = 0
punch_time_E = 0
Player_Health = 3

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
        if self.rect.top < SCREEN_HEIGHT:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom > 0:
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
        #Get the position of the mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #Replace it with crosshair (Need to update)
        screen.blit(mousec, (mouse_x, mouse_y))
        #Find the relative distance (normalized) from mouse to player
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        # Use tangent to find the angle that the sprite needs to be moved to face the mouse
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90  
        #This is a new image that rotates the old image
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        #This is the position of the old image
        rect = self.image.get_rect(center=self.rect.center)   
        #Put the new image in the same place as the old image
        screen.blit(self.newimage,rect)
        pygame.display.update()

    def punch(self):
        self.image = pygame.image.load("King_Punch.png")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #Replace it with crosshair (Need to update)
        screen.blit(mousec, (mouse_x, mouse_y))
        #Find the relative distance (normalized) from mouse to player
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        # Use tangent to find the angle that the sprite needs to be moved to face the mouse
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90  
        #This is a new image that rotates the old image
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        #This is the position of the old image
        rect = self.image.get_rect(center=self.rect.center)   
        #Put the new image in the same place as the old image
        screen.blit(self.newimage,rect)
        pygame.display.update()

    def knockback(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #Replace it with crosshair (Need to update)
        screen.blit(mousec, (mouse_x, mouse_y))
        #Find the relative distance (normalized) from mouse to player
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.rect.move_ip(-rel_x*.1, -rel_y*.1)
        

                
            
                


class Enemy(pygame.sprite.Sprite):
    def __init__(self, Player):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.last = pygame.time.get_ticks()
        self.player = Player
        self.rect = self.image.get_rect()
        self.rect.center=(SCREEN_WIDTH/2, 100) 
        



 
    def move(self):
        # Find direction vector (dx, dy) between enemy and player.
        

        dirvect = pygame.math.Vector2(self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)

        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        self.speed = 3
        dirvect.scale_to_length(self.speed)
        self.rect.move_ip(dirvect)

    def stop(self):
        #So that if the enemy gets within punching distance, it stops
         self.rect.move_ip(0,0)


    def look(self):

        # Look at the player that the enemy is attacking 
        dirvect = pygame.math.Vector2(self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y)
        angle = (180 / math.pi) * math.atan2(dirvect.x, dirvect.y)
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        rect = self.image.get_rect(center=self.rect.center)   
        screen.blit(self.newimage,rect)
        pygame.display.update()

    def punch(self):

        # Look at the player that the enemy is attacking 
        self.image = pygame.image.load("Enemy_Punch.png")
        dirvect = pygame.math.Vector2(self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y)
        angle = (180 / math.pi) * math.atan2(dirvect.x, dirvect.y)
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        rect = self.image.get_rect(center=self.rect.center)   
        screen.blit(self.newimage,rect)
        pygame.display.update()

        

    def reset_sprite(self):
        self.image = pygame.image.load("Enemy.png")
        dirvect = pygame.math.Vector2(self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y)
        angle = (180 / math.pi) * math.atan2(dirvect.x, dirvect.y)
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        rect = self.image.get_rect(center=self.rect.center)   
        screen.blit(self.newimage,rect)
        pygame.display.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect) 

    def knockback(self):
        dirvect = pygame.math.Vector2(self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y)
        self.rect.move_ip(dirvect*.4)


class Stationary(pygame.sprite.Sprite):       
    def __init__(self, vector):
        super().__init__() 
        self.image = pygame.image.load("Chair_sprite.png")
        self.rect = self.image.get_rect()
        self.rect.center = (vector) 

    def draw(self, surface):
        surface.blit(self.image, self.rect) 
        pygame.display.update()

P1 = Player()
E1 = Enemy(P1)
C1 = Stationary((160, 420))
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1)


while True:
    pygame.display.update()
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == event.type == MOUSEBUTTONDOWN and event.button == 1:
                punch_time = pygame.time.get_ticks()
                P1.punch()
                if pygame.sprite.spritecollideany(P1, enemies):
                    E1.knockback()
            elif event.type == event.type == MOUSEBUTTONDOWN and event.button == 3:
                print("test3")
    
    screen.fill(WHITE)
    P1.move()
    C1.draw(screen)
    P1.look()
    E1.look()
    

    if current_time - punch_time > 150:
        P1.image = pygame.image.load("King.png")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #Replace it with crosshair (Need to update)
        screen.blit(mousec, (mouse_x, mouse_y))
        #Find the relative distance (normalized) from mouse to player
        rel_x, rel_y = mouse_x - P1.rect.x, mouse_y - P1.rect.y
        # Use tangent to find the angle that the sprite needs to be moved to face the mouse
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90  
        #This is a new image that rotates the old image
        P1.newimage = pygame.transform.rotate(P1.image, int(angle))
        #This is the position of the old image
        rect = P1.image.get_rect(center=P1.rect.center)   
        #Put the new image in the same place as the old image
        screen.blit(P1.newimage,rect)
        pygame.display.update()


    
    if pygame.sprite.spritecollideany(P1, enemies):
        E1.stop()
        if current_time - punch_time_E > 500:
            E1.punch()
            P1.knockback()
            # Because the current_time - punch time will always be 500 or less, the sprite gets replaced immediately. Fix this later
            E1.stop()
        if  current_time - punch_time_E > 600:
            E1.image = pygame.image.load("Enemy.png")
            dirvect = pygame.math.Vector2(E1.rect.x - P1.rect.x, E1.rect.y - P1.rect.y)
            angle = (180 / math.pi) * math.atan2(dirvect.x, dirvect.y)
            E1.newimage = pygame.transform.rotate(E1.image, int(angle))
            rect = E1.image.get_rect(center=E1.rect.center)   
            screen.blit(E1.newimage,rect)
            pygame.display.update()
            E1.stop()
            punch_time_E = pygame.time.get_ticks()
        
    else:
        E1.move()

    if Player_Health == 0:
        screen.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        screen.fill(RED[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        

    

    

    pygame.display.update()
    FramePerSec.tick(FPS) 




