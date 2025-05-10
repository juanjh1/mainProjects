from turns_engeen import Turns

import pygame

pygame.init()

WIDTH = 1280
HEIGTH = 720
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

game_truns = Turns();
exit = False
while(not exit):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")


    pygame.display.flip()

    clock.tick(60)
    


pygame.quit()