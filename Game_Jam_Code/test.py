import pygame
screen=pygame.display.set_mode([640, 480])
screen.fill([255, 255, 255])
red=255
surf = pygame.Surface((162, 100))
pygame.draw.rect(surf, (0, 100, 255, 155), (0, 0, 162, 100), 21)
surf.fill((0, 100, 255, 155))
pygame.display.flip()
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
pygame.quit()