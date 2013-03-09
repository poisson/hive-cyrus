#!/usr/bin/env python

import pygame, sys, os
from pygame.locals import *

import constants
import tile
import sprite
import room
import debug
debug.DEBUG = True

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption(constants.title)

# Load graphics resources here

# light
light = pygame.image.load(os.path.join(constants.graphicspath, constants.lightpath))
light = light.convert_alpha()

# sprites
sprites = []
i = 0
j = 1
tmpimg = None
for spr in os.listdir(os.path.join(constants.graphicspath, constants.spritepath)):
    print spr
    first = True
    for fname in os.listdir(os.path.join(constants.graphicspath, constants.spritepath, spr)):
        tmpimg = pygame.image.load(os.path.join(constants.graphicspath, constants.spritepath, spr, fname))
        tmpimg = tmpimg.convert()
        tmpimg.set_colorkey(pygame.Color(255,0,255))
        if first:
            sprites.append(sprite.Sprite(tmpimg))
            first = False
        else:
            sprites[-1].addimg(tmpimg)

# Load level resources and suchlike here (this may turn out to be temporary)
# rooms
level = room.Room(os.path.join(constants.levelpath, 'empty.hcr'))

left = False
right = False
up = False
down = False
while True: # main loop
    window.fill(pygame.Color(255,255,255))
    pygame.draw.rect(window, (255,0,0), (0,0,39,39))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                left = True
            elif event.key == K_RIGHT:
                right = True
            elif event.key == K_UP:
                up = True
            elif event.key == K_DOWN:
                down = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                left = False
            elif event.key == K_RIGHT:
                right = False
            elif event.key == K_UP:
                up = False
            elif event.key == K_DOWN:
                down = False

    if left:
        sprites[-1].moveleft()
        if pygame.sprite.spritecollide(sprites[-1].pgsprite, level.unwalkable, False) != []:
            sprites[-1].moveright()
    if right:
        sprites[-1].moveright()
        if pygame.sprite.spritecollide(sprites[-1].pgsprite, level.unwalkable, False) != []:
            sprites[-1].moveleft()
    if up:
        sprites[-1].moveup()
        sprites[-1].frame = 1
        if pygame.sprite.spritecollide(sprites[-1].pgsprite, level.unwalkable, False) != []:
            sprites[-1].movedown()
    if down:
        sprites[-1].movedown()
        sprites[-1].frame = 0
        if pygame.sprite.spritecollide(sprites[-1].pgsprite, level.unwalkable, False) != []:
            sprites[-1].moveup()

#    for t in tiles:
#        t.draw(window)

    level.draw(window)

    for s in sprites:
        s.draw(window)

    # Render the light overlay
    window.blit(light, ( (sprites[-1].position[0]*constants.tilesize) - (light.get_width() / 2) + constants.tilesize / 2, (sprites[-1].position[1]*constants.tilesize) - (light.get_height() / 2) + constants.tilesize / 2 ) )

    pygame.display.update()
    clock.tick(30)

