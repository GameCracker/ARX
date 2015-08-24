#!/usr/bin/env python2

## dimension of screen is 1024 * 600

import pygame
from pygame.locals import *

from constants import *

pygame.init()

if fullscreen_on:
    screen = pygame.display.set_mode(size, FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)

from drawstuff import *


def draw():
    screen.fill(background_color)

    left = pygame.Rect(usable_x, usable_y, usable_width_1, usable_height)
    right = pygame.Rect(split_x, usable_y, usable_width_1, usable_height)

    pygame.draw.rect(screen, red, left)
    pygame.draw.rect(screen, green, right)

    pygame.display.flip()

while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:  # Window close button clicked?
        break
    elif ev.type == pygame.KEYDOWN:
        if ev.key == K_ESCAPE:
            break

    draw()
        
