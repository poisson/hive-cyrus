#!/usr/bin/env python

import pygame, sys, os, socket, pickle
from pygame.locals import *

import constants
import tile
import sprite, zsprite
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
tmpimg = None
first = True
i = 0
for fname in os.listdir(os.path.join(constants.graphicspath, constants.spritepath, constants.playerpath)):
    tmpimg = pygame.image.load(os.path.join(constants.graphicspath, constants.spritepath, constants.playerpath, fname))
    tmpimg = tmpimg.convert()
    tmpimg.set_colorkey(pygame.Color(255,0,255))
    if first:
        player = sprite.Sprite(tmpimg, i)
        first = False
    else:
        player.addimg(tmpimg, i)
    i += 1
    if (i % 4) == 0:
        i = 0

first = True
for fname in os.listdir(os.path.join(constants.graphicspath, constants.spritepath, constants.queenpath)):
    tmpimg = pygame.image.load(os.path.join(constants.graphicspath, constants.spritepath, constants.queenpath, fname))
    tmpimg = tmpimg.convert()
    tmpimg.set_colorkey(pygame.Color(255,0,255))
    if first:
        queen = zsprite.zSprite(tmpimg)
        first = False
    else:
        queen.addimg(tmpimg)

# Load level resources and suchlike here (this may turn out to be temporary)
# rooms
level = room.Room(os.path.join(constants.levelpath, 'empty.hcr'))

# Set up socket for multiplayer
serv = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
serv.bind(('localhost', 5432))
serv.listen(5)

pygame.mixer.music.load(os.path.join(constants.musicpath, 'HiveCyrus.ogg'))
pygame.mixer.music.play(-1)

print "Waiting..."
(sock, address) = serv.accept()
print "Connected!"

children = []
babygroup = pygame.sprite.Group()
left = False
right = False
up = False
down = False
rotation = -1
direction = 0
drawlight = None
while True: # mainloop
    zerg = [queen] + children
    window.fill(pygame.Color(255,255,255))

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
            elif event.key == K_s:
                direction = 0
            elif event.key == K_a:
                direction = 1
            elif event.key == K_w:
                direction = 2
            elif event.key == K_d:
                direction = 3
        if event.type == KEYUP:
            if event.key == K_LEFT:
                left = False
            elif event.key == K_RIGHT:
                right = False
            elif event.key == K_UP:
                up = False
            elif event.key == K_DOWN:
                down = False

    player.direction = direction

    if left:
        player.moveleft()
        if pygame.sprite.spritecollide(player.pgsprite, level.unwalkable, False) != []:
            player.moveright()
    if right:
        player.moveright()
        if pygame.sprite.spritecollide(player.pgsprite, level.unwalkable, False) != []:
            player.moveleft()
    if up:
        player.moveup()
        if pygame.sprite.spritecollide(player.pgsprite, level.unwalkable, False) != []:
            player.movedown()
    if down:
        player.movedown()
        if pygame.sprite.spritecollide(player.pgsprite, level.unwalkable, False) != []:
            player.moveup()
    try:
        zpos = pickle.loads(sock.recv(1024))
        sock.send(pickle.dumps([player.position, player.direction]))
    except:
        pygame.quit()
        sys.exit("Other half closed")

    queen.position = zpos[0]
    for i in range(0, len(zpos[1:])):
        if len(children) <= i:
            first = True
            for fname in os.listdir(os.path.join(constants.graphicspath, constants.spritepath, constants.dronepath)):
                tmpimg = pygame.image.load(os.path.join(constants.graphicspath, constants.spritepath, constants.dronepath, fname))
                tmpimg = tmpimg.convert()
                tmpimg.set_colorkey(pygame.Color(255,0,255))
                if first:
                    children.append(zsprite.zSprite(tmpimg, (queen.position[0] + 1, queen.position[1])))
                    first = False
                else:
                    children[-1].addimg(tmpimg)
            babygroup.add(children[-1].pgsprite)
        children[i].position = zpos[i+1]

    level.draw(window)

    for z in zerg:
        z.draw(window)

    if rotation != direction:
        rotation = direction
        drawlight = pygame.transform.rotate(light, direction * -90)

    # Render the light overlay
    window.blit(drawlight, ( (player.position[0]*constants.tilesize) - (light.get_width() / 2) + constants.tilesize / 2, (player.position[1]*constants.tilesize) - (light.get_height() / 2) + constants.tilesize / 2 ) )

    player.draw(window)

    pygame.display.update()
    clock.tick(30)

