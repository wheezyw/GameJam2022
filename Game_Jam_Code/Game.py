import sys
import os
import pygame.locals
os.path.join(r"GameJam2022", r"Images")
# import the pygame module, so you can use it
import pygame
 
# define a main function
def main():
    

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load(r"Logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Battle Royale")
     
   
    # create a surface on screen that has the size of 300 x 300
    screen = pygame.display.set_mode((300,300))

    # Make a movable character
    image = pygame.image.load("Guy.png")
    screen.blit(image, (50,50))
    pygame.display.flip()

    # Making colors, the numbers correspond to RGB values
    color1 = pygame.Color(0, 0, 0)         # Black
    color2 = pygame.Color(255, 255, 255)   # White
    color3 = pygame.Color(128, 128, 128)   # Grey
    color4 = pygame.Color(255, 0, 0)       # Red 

    FPS = pygame.time.Clock()
    FPS.tick(60)
     
    # This is the while loop that keeps the game running, every time that an event happens, this loop checks if that event was quitting. If it was, the game quits. 
    while True:
        pygame.display.update()
        for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
     
   
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()