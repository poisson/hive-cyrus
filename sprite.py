import constants
import pygame

class Sprite:
    pgsprite = None
    images = [[], [], [], []]
    frame = 0
    position = (2,2)
    speed = .2
    # 0 is down, 1 is left, 2 is up, 3 is right
    direction = 0

    def draw(self, window):
        window.blit(self.images[self.direction][self.frame], (self.position[0]*constants.tilesize, self.position[1]*constants.tilesize))
        self.frame += 1
        if (self.frame % len(self.images[self.direction])) == 0:
            self.frame = 0

    def __init__(self, img, direct, pos=(2,2)):
        print direct
        self.pgsprite = pygame.sprite.Sprite()
        self.images[direct].append(img)
        self.pgsprite.image = img
        self.pgsprite.rect = pygame.Rect(pos[0]*constants.tilesize, pos[1]*constants.tilesize, constants.tilesize, constants.tilesize)
        self.position = pos
        self.frame = 0

    def addimg(self, surf, direct):
        print self.images
        self.images[direct].append(surf)

    def setpos(self, pos):
        if pos[0] < 0:
            pos = (0, pos[1])
        if pos[1] < 0:
            pos = (pos[0], 0)
        if pos[0] > constants.windowwidth:
            pos = (constants.windowwidth, pos[1])
        if pos[1] > constants.windowheight:
            pos = (pos[0], constants.windowheight)
        self.position = pos
        self.pgsprite.rect = pygame.Rect(pos[0]*constants.tilesize, pos[1]*constants.tilesize, constants.tilesize, constants.tilesize)

    def moveright(self):
        if self.direction != 3:
            self.direction = 3
        self.setpos((self.position[0] + self.speed, self.position[1]))

    def moveleft(self):
        if self.direction != 1:
            self.direction = 1
        self.setpos((self.position[0] - self.speed, self.position[1]))

    def moveup(self):
        if self.direction != 2:
            self.direction = 2
        self.setpos((self.position[0], self.position[1] - self.speed))

    def movedown(self):
        if self.direction != 0:
            self.direction = 0
        self.setpos((self.position[0], self.position[1] + self.speed))
