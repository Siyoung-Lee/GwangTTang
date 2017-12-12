import pygame
import random

from pico2d import *

character_img = pygame.image.load("character\\character_1.png")

def main():
    pygame.init()

    screen = pygame.display.set_mode([1200, 700])

    while 1:
        screen.fill(0)
        screen.blit(character_img, (100, 100))




if __name__ == '__main__':
    main()
