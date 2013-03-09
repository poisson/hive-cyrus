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

## tiles
#tiles = []
#i = 1
#j = 0
#for fname in os.listdir(os.path.join(constants.graphicspath, constants.tilepath)):
#    tiles.append(tile.Tile(pygame.image.load(os.path.join(constants.graphicspath, constants.tilepath, fname)), fname, [(i, j)])) # position loading here is temporary for display purposes
#    tiles[-1].surface.convert()
#    i += 1
#    if i % (800/constants.tilesize) == 0:
#        i = 0
#        j += 1

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
        tmpimg.convert()
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

    print pygame.sprite.spritecollide(sprites[-1].pgsprite, level.unwalkable, False)
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
        if pygame.sprite.spritecollide(sprites[-1].pgsprite, level.unwalkable, False) != []:
            sprites[-1].movedown()
    if down:
        sprites[-1].movedown()
        if pygame.sprite.spritecollide(sprites[-1].pgsprite, level.unwalkable, False) != []:
            sprites[-1].moveup()

#    for t in tiles:
#        t.draw(window)

    level.draw(window)

    for s in sprites:
        s.draw(window)

    pygame.display.update()
    clock.tick(30)

