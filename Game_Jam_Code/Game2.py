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
Player_Health = 100

# Making colors, the numbers correspond to RGB values
BLACK = pygame.Color(0, 0, 0)         # Black
WHITE = pygame.Color(255, 255, 255)   # White
GREY = pygame.Color(128, 128, 128)   # Grey
RED = pygame.Color(255, 0, 0)       # Red 
YELLOW = pygame.Color(62, 63, 10)

 # create a surface on screen that has the size of 400 x 600
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)

# load and set the logo
logo = pygame.image.load("Images/Logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Battle Royale")


#Make mouse crosshair
pygame.mouse.set_visible(False)
mousec = pygame.image.load("Images/mouse_C.png").convert_alpha()

# make background

#Sprite Number controls the weapons that the player is holding and the animations
Sprite_number = 0



#Controls the Main Loop
main = True

# Make "Mouse Collision" function
def mouse_collision(topleft, bottomright):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if topleft[1] - mouse_y <  0 and  bottomright[1] - mouse_y > 0 and topleft[0] - mouse_x < 0 and bottomright[0] - mouse_x > 0:
        return True

#Make Classes

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        if Sprite_number == 0:
            self.image = pygame.image.load("Images/King.png")
        if Sprite_number == 1:
            self.image = pygame.image.load("Images/King_holding_chair.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:
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
        if Sprite_number == 0:
            self.image = pygame.image.load("Images/King_Punch.png")
        if Sprite_number == 1:
            self.image = pygame.image.load("Images/King_chair_swing_2.png")
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
        if self.rect.top > 0 and self.rect.bottom < SCREEN_HEIGHT and self.rect.left > 0 and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(-rel_x*.1, -rel_y*.1)
        else:
            self.rect.move_ip(0, 0)
        
    def playerdeath(self):
        self.image = pygame.image.load("Images/King_Dead_64.png")
        pygame.display.update()
                
            
                


class Enemy(pygame.sprite.Sprite):
    def __init__(self, Player, vector):
        super().__init__() 
        self.image = pygame.image.load("Images/Enemy.png")
        self.last = pygame.time.get_ticks()
        self.player = Player
        self.rect = self.image.get_rect()
        self.rect.center= (vector) 
        
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
        self.image = pygame.image.load("Images/Enemy_Punch.png")
        dirvect = pygame.math.Vector2(self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y)
        angle = (180 / math.pi) * math.atan2(dirvect.x, dirvect.y)
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        rect = self.image.get_rect(center=self.rect.center)   
        screen.blit(self.newimage,rect)
        pygame.display.update()

        

    def reset_sprite(self):
        self.image = pygame.image.load("Images/Enemy.png")
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

        if self.rect.top > 0 and self.rect.bottom < SCREEN_HEIGHT and self.rect.left > 0 and self.rect.right < SCREEN_WIDTH:
            if Sprite_number == 0:
                if  SCREEN_WIDTH - self.rect.x + dirvect.x*.4 > 0 and SCREEN_WIDTH - self.rect.x + dirvect.x*.4 < SCREEN_WIDTH and SCREEN_HEIGHT - self.rect.y + dirvect.y*.4 > 0 and SCREEN_HEIGHT - self.rect.y + dirvect.y < SCREEN_HEIGHT:
                    self.rect.move_ip(dirvect*.4)
                elif SCREEN_WIDTH - self.rect.x + dirvect.x*.4 < 0 :
                    self.rect.move_ip(SCREEN_WIDTH - 50, dirvect.y*.4)
                elif SCREEN_WIDTH - self.rect.x + dirvect.x*.4> SCREEN_WIDTH:
                    self.rect.move_ip(50, dirvect.y*.4)
                elif SCREEN_HEIGHT - self.rect.y + dirvect.y*.4 < 0 :
                    self.rect.move_ip(dirvect.x, SCREEN_HEIGHT - 50)
                elif SCREEN_HEIGHT - self.rect.y + dirvect.y > SCREEN_HEIGHT:
                    self.rect.move_ip(dirvect.x, 50)
            if Sprite_number == 1:
                if  SCREEN_WIDTH - (self.rect.x + dirvect.x*1.5) > 0 and SCREEN_WIDTH - (self.rect.x + dirvect.x*1.5) < SCREEN_WIDTH and SCREEN_HEIGHT - (self.rect.y + dirvect.y*1.5) > 0 and SCREEN_HEIGHT - (self.rect.y + dirvect.y*1.5) < SCREEN_HEIGHT:
                    self.rect.move_ip(dirvect*1.5)
                elif SCREEN_WIDTH - (self.rect.x + dirvect.x*1.5) < 0 :
                    self.rect.move_ip(SCREEN_WIDTH - 50, dirvect.y*1.5)
                elif SCREEN_WIDTH - (self.rect.x + dirvect.x*1.5)> SCREEN_WIDTH:
                    self.rect.move_ip(50, dirvect.y*1.5)
                elif SCREEN_HEIGHT - (self.rect.y + dirvect.y*1.5)  < 0 :
                    self.rect.move_ip(dirvect.x* 1.5, SCREEN_HEIGHT - 50)
                elif SCREEN_HEIGHT - (self.rect.y + dirvect.y * 1.5)> SCREEN_HEIGHT:
                    self.rect.move_ip(dirvect.x * 1.5, 50)
        else:
            self.rect.move_ip(0, 0)
        
        


class Stationary(pygame.sprite.Sprite):       
    def __init__(self, vector, image):
        super().__init__() 
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (vector) 

    def draw(self, surface):
        surface.blit(self.image, self.rect) 
        pygame.display.update()

    def stop(self):
        #So that if the enemy gets within punching distance, it stops
         self.rect.move_ip(0,0)




P1 = Player()
E1 = Enemy(P1, (400, 600))
E2 = Enemy(P1, (600, 600))
Chair1 = Stationary((160, 420), "Images/Chair_sprite.png" )
No_Button = Stationary ((700, 575), "Images/No_3.png")
Yes_Button = Stationary((300, 575), "Images/Yes_4.png")
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1, E2)
stationaries = pygame.sprite.Group()
stationaries.add(Chair1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, enemies, stationaries)


# Make reset event 
def Game_reset():
    P1.rect.center = (160, 520)
    E1.rect.center=  (400, 600)
    E1.image = pygame.image.load("Images/Enemy.png")
    E2.rect.center=  (600, 600)
    E2.image = pygame.image.load("Images/Enemy.png")
    Chair1.rect.center = (160, 420)
    Chair1.image = pygame.image.load("Images/Chair_sprite.png")
    

while main:
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
                if pygame.sprite.spritecollideany(P1, enemies):
                    E2.knockback()
            elif event.type == event.type == MOUSEBUTTONDOWN and event.button == 3:
                if pygame.sprite.spritecollideany(P1, stationaries):
                    if Sprite_number == 0:
                        Sprite_number = 1
                        Chair1.image = pygame.image.load("Images/clear_block.png")
                        Chair1.rect.center = (SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2)
                elif Sprite_number == 1:
                    Sprite_number = 0
                    Chair1.image = pygame.image.load("Images/Chair_sprite.png")
                    Chair1.rect.center = (P1.rect.x + 50, P1.rect.y)
    
    screen.fill(WHITE)
    P1.move()
    Chair1.draw(screen)
    P1.look()
    E1.look()
    E2.look()
    print(current_time - punch_time_E)
    

    if current_time - punch_time > 150:
        if Sprite_number == 0:
            P1.image = pygame.image.load("Images/King.png")
        if Sprite_number == 1:
            P1.image = pygame.image.load("Images/King_holding_chair.png")
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
        if current_time - punch_time_E > 800:
            E1.punch()
            print("punch")
            punch_time_E = pygame.time.get_ticks()
            P1.knockback()
            # Because the current_time - punch time will always be 500 or less, the sprite gets replaced immediately. Fix this later
            E1.stop()
            Player_Health -= 100
            print(Player_Health)
        if  current_time - punch_time_E > 200:
            print("no punch")
            print(current_time - punch_time_E)
            E1.image = pygame.image.load("Images/Enemy.png")
            dirvect = pygame.math.Vector2(E1.rect.x - P1.rect.x, E1.rect.y - P1.rect.y)
            angle = (180 / math.pi) * math.atan2(dirvect.x, dirvect.y)
            E1.newimage = pygame.transform.rotate(E1.image, int(angle))
            rect = E1.image.get_rect(center=E1.rect.center)   
            screen.blit(E1.newimage,rect)
            pygame.display.update()
            E1.stop()
    
    
    
    else:
        E1.move()

    if Player_Health == 0:
        Game_Over_Screen = pygame.image.load("Images/Game_Over_Screen2.png")
        Game_Over_Screen = pygame.transform.scale(Game_Over_Screen, (1000,1000))
        GOScreen_rect = Game_Over_Screen.get_rect()
        screen.blit(Game_Over_Screen, GOScreen_rect)
        E1.stop()
        P1.playerdeath()
        main = False
        while main == False:
            screen.blit(Game_Over_Screen, GOScreen_rect)
            screen.blit(No_Button.image, No_Button.rect)
            screen.blit(Yes_Button.image, Yes_Button.rect)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #Replace it with crosshair (Need to update)
            screen.blit(mousec, (mouse_x, mouse_y))
            pygame.display.update() 
            if mouse_collision(No_Button.rect.topleft, No_Button.rect.bottomright):
                # Replace the Button with Yellow highlighted Button, same with Yes Button
                if  event.type == event.type == MOUSEBUTTONDOWN and event.button == 1:
                    pygame.quit()
                    sys.exit()
            if mouse_collision(Yes_Button.rect.topleft, Yes_Button.rect.bottomright):
                if  event.type == event.type == MOUSEBUTTONDOWN and event.button == 1:
                    print("Yes")
                    Game_reset()
                    Player_Health = 100
                    Sprite_number = 0
                    punch_time_E = pygame.time.get_ticks()
                    main = True
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
    

    

    pygame.display.update()
    FramePerSec.tick(FPS) 




