#!/usr/bin/env python2

import pygame, sys
from constants import *

font_path = pygame.font.match_font('Arial')

def draw_text(text, center, color=white, size=22, bold=False, background=None,
              left=False):
    font = pygame.font.Font(font_path, size, bold=bold)
    if background:
        surface = font.render(text, True, color, background)
    else:
        surface = font.render(text, True, color)

    rect = surface.get_rect()
    rect.center = tuple(center)
    if left:
        rect.left = center[0]

    screen.blit(surface, rect)
    return rect

def draw_image(img, center):
    rect = img.get_rect()
    rect.center = tuple(center)
    screen.blit(img, rect)
