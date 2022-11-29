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
punch_time = 400
punch_time_E = 0
Player_Health = 100
P1_Punched = 1
bg = pygame.image.load("Images/stage.png")
chairthrow = 0
holding_chair = 0
Game_Over = 0

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

# Make a Time function that executes a function once every x milliseconds

def Timer(milliseconds, timerTime):
    if current_time - timerTime > milliseconds:
        return True
    else:
        return False


# Make "Mouse Collision" function
def mouse_collision(topleft, bottomright):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if topleft[1] - mouse_y <  0 and  bottomright[1] - mouse_y > 0 and topleft[0] - mouse_x < 0 and bottomright[0] - mouse_x > 0:
        return True

#Performs vector arithmetics
class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v):
        x = self.x + v.x
        y = self.y + v.y
        return Vector(x, y)

#Make Classes

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        if Sprite_number == 0:
            self.image = pygame.image.load("Images/RedIdle.png")
        if Sprite_number == 1:
            self.image = pygame.image.load("Images/King_holding_chair.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.isdead = False
        
  
    def move(self): 
        pressed_keys = pygame.key.get_pressed() 
        if self.rect.top > 0: 
            if pressed_keys[K_w]: 
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_s]:
                self.rect.move_ip(0,5)

          
        if self.rect.left > 0:
              if pressed_keys[K_a]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_d]:
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
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)   
        #print(angle)
        #This is a new image that rotates the old image
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        #This is the position of the old image
        rect = self.image.get_rect(center=self.rect.center)   
        #Put the new image in the same place as the old image
        screen.blit(self.newimage,rect)

    def beforePunch(self):
        if Sprite_number == 0:
            self.image = pygame.image.load("Images/RedPunch.png")
        if Sprite_number == 1:
            self.image = pygame.image.load("Images/King_chair_swing_2.png")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #Replace it with crosshair (Need to update)
        screen.blit(mousec, (mouse_x, mouse_y))
        #Find the relative distance (normalized) from mouse to player
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        # Use tangent to find the angle that the sprite needs to be moved to face the mouse
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)   
        #This is a new image that rotates the old image
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        #This is the position of the old image
        rect = self.image.get_rect(center=self.rect.center)   
        #Put the new image in the same place as the old image
        screen.blit(self.newimage,rect)

    def punch(self):
        if Sprite_number == 0:
            self.image = pygame.image.load("Images/RedPunch2.png")
        if Sprite_number == 1:
            self.image = pygame.image.load("Images/King_chair_swing_2.png")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #Find the relative distance (normalized) from mouse to player
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        # Use tangent to find the angle that the sprite needs to be moved to face the mouse
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)  
        #This is a new image that rotates the old image
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        #This is the position of the old image
        rect = self.image.get_rect(center=self.rect.center)   
        #Put the new image in the same place as the old image
        screen.blit(self.newimage,rect)


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
        self.isdead = True

    
       
                


class Enemy(pygame.sprite.Sprite):
    def __init__(self, Player, vector):
        super().__init__() 
        self.image = pygame.image.load("Images/GreenIdle.png")
        self.last = pygame.time.get_ticks()
        self.player = Player
        self.rect = self.image.get_rect()
        self.rect.center= (vector) 
        self.isdead = False


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


    def look(self, object):

        # Look at the player that the enemy is attacking 
        dirvect = pygame.math.Vector2(self.rect.x - object.rect.x, self.rect.y - object.rect.y)
        angle = (180 / math.pi) * math.atan2(dirvect.x, dirvect.y) + 90
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        rect = self.image.get_rect(center=self.rect.center)   
        screen.blit(self.newimage,rect)

    def beforePunch(self):
        if Sprite_number == 0:
            self.image = pygame.image.load("Images/GreenPunch.png")
        #if Sprite_number == 1:
            
        dirvect = pygame.math.Vector2(self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y)
        angle = (180 / math.pi) * math.atan2(dirvect.x, dirvect.y) + 90
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        #This is the position of the old image
        rect = self.image.get_rect(center=self.rect.center)   
        #Put the new image in the same place as the old image
        screen.blit(self.newimage,rect)

    def punch(self):

        # Look at the player that the enemy is attacking 
        self.image = pygame.image.load("Images/GreenPunch3.png")
        dirvect = pygame.math.Vector2(self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y)
        angle = (180 / math.pi) * math.atan2(dirvect.x, dirvect.y) 
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        rect = self.image.get_rect(center=self.rect.center)   
        screen.blit(self.newimage,rect)


        

    def reset_sprite(self):
        self.image = pygame.image.load("Images/GreenIdle.png")
        dirvect = pygame.math.Vector2(self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y)
        angle = (180 / math.pi) * math.atan2(dirvect.x, dirvect.y) + 90
        self.newimage = pygame.transform.rotate(self.image, int(angle))
        rect = self.image.get_rect(center=self.rect.center)   
        screen.blit(self.newimage,rect)


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
        
    def death(self):
        E1.image = pygame.image.load("Images/Enemy_Dead.png")
        E1.stop()
        self.isdead = True
    

        
        


class Stationary(pygame.sprite.Sprite):       
    def __init__(self, vector, image):
        super().__init__() 
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (vector) 

    def draw(self, surface):
        surface.blit(self.image, self.rect) 


    def stop(self):
        #So that if the enemy gets within punching distance, it stops
         self.rect.move_ip(0,0)

    def throw(self, rel_x, rel_y, chair_mouse_x, chair_mouse_y):
        
        angle =  math.atan2(rel_y, rel_x)
        
        angle_x = math.cos(angle)
        
       
        angle_y = math.sin(angle)
        #print(chair_mouse_x)
        #print(chair_mouse_y)
        #print(angle_x)
       # print(angle_y)
        if self.rect.x < chair_mouse_x-10:
            self.rect.move_ip(angle_x * 10, 0)
            #Chair1.rect.move_ip(5, 0)
            #print("moving right")
           # print(Chair1.rect.x)
            #print(chair_mouse_x)
        elif self.rect.x > chair_mouse_x+10:
            self.rect.move_ip(angle_x * 10, 0)
            
            #Chair1.rect.move_ip(-5, 0)
            #print("moving left")
            #print(Chair1.rect.x)
            #print(chair_mouse_x)
        elif self.rect.x == range(chair_mouse_x-10, chair_mouse_x+10):
            self.rect.move_ip(0,0)
        if self.rect.y > chair_mouse_y+10:
            self.rect.move_ip(0, angle_y * 10)
            #Chair1.rect.move_ip(0, 5)
            #print("moving up")
            #print(Chair1.rect.y)
            #print(chair_mouse_y)
        elif self.rect.y < chair_mouse_y-10:
            self.rect.move_ip(0, angle_y * 10)
            #Chair1.rect.move_ip(0, -5)
            #print("moving down")
            #print(Chair1.rect.y)
            #print(chair_mouse_y)
        elif self.rect.y == range(chair_mouse_y-10, chair_mouse_y+10):
            self.rect.move_ip(0,0)
        
        

P1 = Player()


E1 = Enemy(P1, (400, 600))
E1_Health = 100
E2 = Enemy(P1, (600, 600))
E2_Health = 100


chair = pygame.image.load("Images/Chair_sprite.png")
chair = pygame.transform.scale(chair, (50,50))
chair_left = pygame.transform.rotate(chair, 90)
chair_right = pygame.transform.rotate(chair, -90)
Chair1 = Stationary((225, 250), chair_right )
Chair1_pos = (225, 250)
Chair2 = Stationary((225, 350), chair_right )
Chair2_pos = (225, 350)
Chair3 = Stationary((225, 450), chair_right )
Chair3_pos = (225, 450)
Chair4 = Stationary((225, 550), chair_right )
Chair4_pos = (225, 550)
Chair5 = Stationary((385, 250), chair_left )
Chair5_pos = (385, 250)
Chair6 = Stationary((385, 350), chair_left )
Chair6_pos = (385, 350)
Chair7 = Stationary((385, 450), chair_left )
Chair7_pos = (385, 450)
Chair8 = Stationary((385, 550), chair_left )
Chair8_pos = (385, 550)

Chair9 = Stationary((625, 250), chair_right )
Chair9_pos = (625, 250)
Chair10 = Stationary((625, 350), chair_right )
Chair10_pos = (625, 350)
Chair11 = Stationary((625, 450), chair_right )
Chair11_pos = (625, 450)
Chair12 = Stationary((625, 550), chair_right )
Chair12_pos = (625, 550)
Chair13 = Stationary((785, 250), chair_left )
Chair13_pos = (785, 250)
Chair14 = Stationary((785, 350), chair_left )
Chair14_pos = (785, 350)
Chair15 = Stationary((785, 450), chair_left )
Chair15_pos = (785, 450)
Chair16 = Stationary((785, 550), chair_left )
Chair16_pos = (785, 550)

table = pygame.image.load("Images/Table.png")
table = pygame.transform.scale(table, (400,400))
Table1 = Stationary((300, 400), table)
Table1_left = 270
Table1_right = 320
Table1_top = 235
Table1_bottom = 550
Table2 = Stationary((700, 400), table)
Table2_left = 670
Table2_right = 720
Table2_top = 235
Table2_bottom = 550

candle = pygame.image.load("Images/candle_stick.png")
candle = pygame.transform.scale(candle, (100,100))
Candle1 = Stationary((305, 450), candle)
Candle2 = Stationary((305, 550), candle)
Candle3 = Stationary((305, 350), candle)
Candle4 = Stationary((305, 250), candle)

Candle5 = Stationary((705, 450), candle)
Candle6 = Stationary((705, 550), candle)
Candle7 = Stationary((705, 350), candle)
Candle8 = Stationary((705, 250), candle)

bottle = pygame.image.load("Images/Bottle.png")
bottle = pygame.transform.scale(bottle, (150,150))
Bottle1 = Stationary((400, 500), bottle)

pot = pygame.image.load("Images/Pot.png")
pot = pygame.transform.scale(pot, (150,150))
Pot1 = Stationary((400, 550), pot)

turkey = pygame.image.load("Images/Turkey.png")
turkey = pygame.transform.scale(turkey, (250,250))
Turkey1 = Stationary((400, 600), turkey)



No_Button = Stationary ((700, 575), pygame.image.load("Images/No_3.png"))
Yes_Button = Stationary((300, 575), pygame.image.load("Images/Yes_4.png"))

#Creating Sprites Groups
enemies = [E1, E2]
chairs = [Chair1,Chair2,Chair3,Chair4,Chair5,Chair6,Chair7,Chair8,Chair9, Chair10, Chair11, Chair12, Chair13, Chair14, Chair15, Chair16]
candles = [Candle1, Candle2, Candle3, Candle4, Candle5, Candle6, Candle7, Candle8]
tables = [Table1, Table2]
characters = [P1, E1]


# Make reset event 
def Game_reset():
    
    P1.rect.center = (160, 520)

    E1.rect.center=  (400, 600)
    E1.image = pygame.image.load("Images/GreenIdle.png")
    E1.isdead = False

    E2.rect.center=  (600, 600)
    E2.image = pygame.image.load("Images/Enemy.png")
    E2.isdead = False

    Chair1.rect.center=  Chair1_pos
    Chair1.image = chair_right
    Chair2.rect.center=  Chair2_pos
    Chair2.image = chair_right
    Chair3.rect.center=  Chair3_pos
    Chair3.image = chair_right
    Chair4.rect.center=  Chair4_pos
    Chair4.image = chair_right

    Chair5.rect.center=  Chair5_pos
    Chair5.image = chair_left
    Chair6.rect.center=  Chair6_pos
    Chair6.image = chair_left
    Chair7.rect.center=  Chair7_pos
    Chair7.image = chair_left
    Chair8.rect.center=  Chair8_pos
    Chair8.image = chair_left

     #An attempt to be smart, that failed. Doing this the manual way.
    '''for i in [Chair1,Chair2,Chair3,Chair4]:
        print(i)
        j = 0
        print (j)
        k = [Chair1_pos,Chair2_pos,Chair3_pos,Chair4_pos]
        i.image = chair_right
        i.rect.center =  k[j]
        j+=1

    for x in [Chair5,Chair6,Chair7,Chair8]:
        print(x)
        y = 0
        print (y)
        z = [Chair5_pos,Chair6_pos,Chair7_pos,Chair8_pos]
        x.image = chair_left
        x.rect.center =  z[y]
        y+=1'''



while main:
    pygame.display.flip()
    screen.fill(WHITE)
    bg = pygame.transform.scale(bg, (1000,1000))
    bg_rect = bg.get_rect()
    screen.blit(bg, bg_rect)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == event.type == MOUSEBUTTONDOWN and event.button == 1 and P1.isdead == False:
                punch_time = pygame.time.get_ticks()
                print(Table1.rect.left )
                print(P1.rect.right - Table1.rect.left)
            elif event.type == event.type == MOUSEBUTTONDOWN and event.button == 3 and P1.isdead == False:
                for held_chair in chairs:
                    if pygame.sprite.collide_rect(P1, held_chair) and holding_chair == 0:
                        current_chair = held_chair
                        print(current_chair.rect.center)
                        print(P1.rect.center)
                        if Sprite_number == 0:
                            Sprite_number = 1
                            oldchair_rect_center = held_chair.rect.center
                            held_chair.image = pygame.image.load("Images/clear_block.png")
                            holding_chair = 1
                            held_chair.rect.center = (SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2)
                            print(current_chair.rect.center)
                            break
                    elif Sprite_number == 1:
                        Sprite_number = 0
                        holding_chair = 0
                        held_chair.image = chair
                        held_chair.rect.center = (P1.rect.x + 50, P1.rect.y)
                        break

            elif event.type == event.type == MOUSEBUTTONDOWN and event.button == 2 and P1.isdead == False:
                if Sprite_number == 1:
                    Sprite_number = 0
                    current_chair.rect.center = (P1.rect.x, P1.rect.y)
                    current_chair.image = chair
                    chair_mouse_x, chair_mouse_y = pygame.mouse.get_pos()
                    
                    chair_rel_x, chair_rel_y = chair_mouse_x - P1.rect.x, chair_mouse_y - P1.rect.y
                    chairthrow = 1
                    holding_chair = 0
    
    
    
    for x in tables:
        x.draw(screen)

    for x in chairs:
        x.draw(screen)

    for x in candles:
        x.draw(screen)

    Bottle1.draw(screen)
    Pot1.draw(screen) 
    Turkey1.draw(screen)

    if P1.isdead == False:
        P1.look()
        P1.move()
    else:
        P1.draw(screen)
    if E1.isdead == False:
        E1.look(P1)
    if E1.isdead == True:
        E1.draw(screen)
    # Make Player Health Display
    font = pygame.font.Font("freesansbold.ttf", 18)
    text = font.render("Player Health: " + str(Player_Health), True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (100, 100)
    screen.blit(text, textRect)
    
    for x in characters:
        if x.rect.right>Table1_left- 10 and x.rect.right< Table1_left+ 10  and (x.rect.top < Table1_bottom and x.rect.bottom > Table1_top):
            x.rect.move_ip(-5, 0)
        if x.rect.left<Table1_right + 10 and x.rect.left> Table1_right-10 and (x.rect.top < Table1_bottom and x.rect.bottom > Table1_top):
            x.rect.move_ip(5, 0)
        if x.rect.bottom<Table1_top + 10 and x.rect.bottom> Table1_top-10 and (x.rect.left < Table1_right and x.rect.right > Table1_left):
            x.rect.move_ip(0, -5)
        if x.rect.top>Table1_bottom - 10 and x.rect.top< Table1_bottom+10 and (x.rect.left < Table1_right and x.rect.right > Table1_left):
            x.rect.move_ip(0, 5)

        if x.rect.right>Table2_left- 10 and x.rect.right< Table2_left+ 10  and (x.rect.top < Table2_bottom and x.rect.bottom > Table2_top):
            x.rect.move_ip(-5, 0)
        if x.rect.left<Table2_right + 10 and x.rect.left> Table2_right-10 and (x.rect.top < Table2_bottom and x.rect.bottom > Table2_top):
            x.rect.move_ip(5, 0)
        if x.rect.bottom<Table2_top + 10 and x.rect.bottom> Table2_top-10 and (x.rect.left < Table2_right and x.rect.right > Table2_left):
            x.rect.move_ip(0, -5)
        if x.rect.top>Table2_bottom - 10 and x.rect.top< Table2_bottom+10 and (x.rect.left < Table2_right and x.rect.right > Table2_left):
            x.rect.move_ip(0, 5)

    if current_time - punch_time < 150 and P1_Punched == 0:
        P1.beforePunch()
    if current_time - punch_time > 150 and current_time - punch_time < 300 and P1_Punched == 0:
        P1.punch()
        if pygame.sprite.collide_rect(P1, E1):
            E1.knockback()
            if Sprite_number == 0:
                E1_Health -= 10
                print(E1_Health)
            if Sprite_number == 1:
                E1_Health -= 30
                print(E1_Health)
        P1_Punched = 1
    if current_time - punch_time > 300 and P1.isdead == False:
        P1_Punched = 0
        if Sprite_number == 0:
            P1.image = pygame.image.load("Images/RedIdle.png")
        if Sprite_number == 1:
            P1.image = pygame.image.load("Images/King_holding_chair.png")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #Replace it with crosshair (Need to update)
        screen.blit(mousec, (mouse_x, mouse_y))
        #Find the relative distance (normalized) from mouse to player
        rel_x, rel_y = mouse_x - P1.rect.x, mouse_y - P1.rect.y
        # Use tangent to find the angle that the sprite needs to be moved to face the mouse
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)  
        #This is a new image that rotates the old image
        P1.newimage = pygame.transform.rotate(P1.image, int(angle))
        #This is the position of the old image
        rect = P1.image.get_rect(center=P1.rect.center)   
        #Put the new image in the same place as the old image
        screen.blit(P1.newimage,rect)
        pygame.display.update()


    
    if pygame.sprite.collide_rect(P1, E1):
        E1.stop()
        if current_time - punch_time_E < 800 and current_time - punch_time_E > 400 and E1.isdead == False:
            E1.beforePunch()
            pygame.display.update()
        if current_time - punch_time_E > 800 and P1.isdead == False and E1.isdead == False:
            E1.punch()
            punch_time_E = pygame.time.get_ticks()
            P1.knockback()
            E1.stop()
            Player_Health -= 10
            pygame.display.update()
        if  current_time - punch_time_E > 200 and current_time - punch_time_E < 400 and P1.isdead == False and E1.isdead == False:
            E1.reset_sprite()
            pygame.display.update()
    elif E1.isdead == False and P1.isdead == False:
        E1.move()

    
    if  current_time - punch_time_E > 200 and pygame.sprite.collide_rect(P1, E1) == False and P1.isdead == False and E1.isdead == False:
        E1.reset_sprite()
    
    if Player_Health <= 0 and Game_Over == 0: 
        P1.playerdeath()
        Game_Over_Time = pygame.time.get_ticks()
        Game_Over = 1

    if E1_Health <= 0 and Game_Over == 0:
        E1.death()
        Game_Over_Time = pygame.time.get_ticks()
        Game_Over = 1
    #Throwing Objects loop
    if chairthrow == 1:
        current_chair.throw(chair_rel_x,chair_rel_y,chair_mouse_x, chair_mouse_y )
        if current_chair.rect.x == chair_mouse_x and current_chair.rect.y == chair_mouse_y:
            chairthrow = 0
    
    for held_chair in chairs:
        if pygame.sprite.collide_rect(held_chair, E1) and chairthrow == 1 and held_chair == current_chair:
            chairthrow = 0
            E1.knockback()
            E1_Health -= 10
    
    
        
    if Game_Over == 1:
        E1.stop()
        print(current_time - Game_Over_Time)
        if current_time - Game_Over_Time > 1000:
            Game_Over_Screen = pygame.image.load("Images/Game_Over_Screen2.png")
            Game_Over_Screen = pygame.transform.scale(Game_Over_Screen, (1000,1000))
            GOScreen_rect = Game_Over_Screen.get_rect()
            screen.blit(Game_Over_Screen, GOScreen_rect)
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
                    E1_Health = 100
                    Sprite_number = 0
                    chairthrow = 0
                    Game_Over = 0
                    punch_time_E = pygame.time.get_ticks()
                    P1.isdead = False
                    main = True
                    
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
    

    
    pygame.display.flip()
    FramePerSec.tick(FPS) 




