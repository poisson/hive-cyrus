#!/usr/bin/env python

import pygame, sys, os, socket, pickle
from time import sleep
from pygame.locals import *

import constants
import tile
import lemons
import sprite, zsprite
import room
import debug
debug.DEBUG = True

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption(constants.title)

# Load graphics resources here

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

lemimg = pygame.image.load(os.path.join(constants.graphicspath, "lemon.bmp"))

# children
children = []
babygroup = pygame.sprite.Group()

# Load level resources and suchlike here (this may turn out to be temporary)
# rooms
level = room.Room(os.path.join(constants.levelpath, 'empty.hcr'))

theme = pygame.mixer.music.load(os.path.join(constants.musicpath, 'HiveCyrus.ogg'))
pygame.mixer.music.play(-1)

selectsound = pygame.mixer.Sound(os.path.join(constants.musicpath, 'drone1.ogg'))
movesound = pygame.mixer.Sound(os.path.join(constants.musicpath, 'drone2.ogg'))

# Set up socket for multiplayer
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
sock.connect(("localhost", 5432))

selected = []
sel = False
rb1 = None
rb2 = None
shift = False
babies_counter = 0
while True: # main loop
    zerg = [queen] + children
    window.fill(pygame.Color(255,255,255))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RSHIFT or event.key == K_LSHIFT:
                shift = True
        if event.type == KEYUP:
            if event.key == K_RSHIFT or event.key == K_LSHIFT:
                shift = False
            elif event.key == K_SPACE and queen in selected:
                # have babies
                babies_counter = 60
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                sel = True
                rb1 = event.pos
                rb2 = rb1
        if event.type == MOUSEMOTION:
            if sel:
                rb2 = event.pos
        if event.type == MOUSEBUTTONUP:
            if event.button == 3:
                movesound.play()
                for s in selected:
                    s.destination = (float(event.pos[0] - constants.tilesize*.5) / constants.tilesize, float(event.pos[1] - constants.tilesize*.5) / constants.tilesize)
            elif event.button == 1:
                selectsound.play()
                sel = False
                selected = []
                for z in zerg:
                    r = pygame.Rect(min(rb1[0], rb2[0]), min(rb1[1], rb2[1]), abs(rb2[0]-rb1[0]), abs(rb2[1]-rb1[1]))
                    if r.colliderect(z.pgsprite.rect):
                        selected.append(z)

    if babies_counter > 0:
        babies_counter -= 1
        if babies_counter == 0:
            # spawn babies
            if children == []:
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
            else:
                children.append(children[-1].clone())
                children[-1].position = (queen.position[0] + 1, queen.position[1])
            children[-1].destination = (queen.position[0], queen.position[1])
            children[-1].pgsprite.rect = queen.pgsprite.rect.copy()
            babygroup.add(children[-1].pgsprite)
    else:
        queen.updatex()
        if pygame.sprite.spritecollideany(queen.pgsprite, level.unwalkable) or pygame.sprite.spritecollideany(queen.pgsprite, babygroup):
            for func in queen.backoff:
                func()
        queen.updatey()
        if pygame.sprite.spritecollideany(queen.pgsprite, level.unwalkable) or pygame.sprite.spritecollideany(queen.pgsprite, babygroup):
            for func in queen.backoff:
                func()

    for c in children:
        c.updatex()
        if pygame.sprite.spritecollide(c.pgsprite, level.unwalkable, False) != [] or pygame.sprite.collide_rect(queen.pgsprite, c.pgsprite) or (pygame.sprite.spritecollide(c.pgsprite, babygroup, False) != [c.pgsprite]):
            for func in c.backoff:
                func()
        c.updatey()
        if pygame.sprite.spritecollide(c.pgsprite, level.unwalkable, False) != [] or pygame.sprite.collide_rect(queen.pgsprite, c.pgsprite) or (pygame.sprite.spritecollide(c.pgsprite, babygroup, False) != [c.pgsprite]):
            for func in c.backoff:
                func()


    zpos = [ z.position for z in zerg ]
    try:
        sock.send(pickle.dumps(zpos))
        st = sock.recv(1024000)
    except:
        pygame.quit()
        sys.exit("Other half closed.")
    st = pickle.loads(st)
    player.position = st[0]
    player.direction = st[1]
    bullets = []
    if st[2] != []:
        for pos in st[2]:
            bullets.append(lemons.Bullet(lemimg, player))
            bullets[-1].setpos(pos)

    for b in bullets:
        deadbabies = pygame.sprite.spritecollide(b.pgsprite, babygroup, False)
        if pygame.sprite.collide_rect(queen.pgsprite, b.pgsprite):
            sleep(2)
            pygame.quit()
            sys.exit("YOU LOSE.")
        if deadbabies != []:
            babygroup.remove(deadbabies)
            children = [x for x in children if not x.pgsprite in deadbabies]
            bullets.remove(b)
        if pygame.sprite.spritecollideany(b.pgsprite, level.unwalkable):
            bullets.remove(b)

    babies = pygame.sprite.spritecollide(player.pgsprite, babygroup, False)
    if babies != []:
        player.lives -= 1
        babygroup.remove(babies)
        children = [x for x in children if not x.pgsprite in babies]

    if player.lives <= 0 or pygame.sprite.collide_rect(player.pgsprite, queen.pgsprite):
        sleep(2)
        pygame.quit()
        sys.exit("YOU WIN.")

    level.draw(window)

    for z in zerg:
        z.draw(window)

    for s in selected:
        pygame.draw.rect(window, (0, 255, 255), (s.position[0]*constants.tilesize, s.position[1]*constants.tilesize, constants.tilesize, constants.tilesize), 1)

    if sel:
        pygame.draw.rect(window, (0, 255, 255), (rb1[0], rb1[1], rb2[0] - rb1[0], rb2[1] - rb1[1]), 1)
    player.draw(window)


    pygame.display.update()
    clock.tick(30)

