import constants
import pygame

class Sprite:
    pgsprite = None
    images = []
    frame = 0
    position = (2,2)
    speed = .2

    def draw(self, window):
        window.blit(self.images[self.frame], (self.position[0]*constants.tilesize, self.position[1]*constants.tilesize))

    def __init__(self, img, pos=(2,2)):
        self.pgsprite = pygame.sprite.Sprite()
        self.images.append(img)
        self.pgsprite.image = img
        self.pgsprite.rect = pygame.Rect(pos[0]*constants.tilesize, pos[1]*constants.tilesize, constants.tilesize, constants.tilesize)
        self.position = pos
        self.frame = 0

    def addimg(self, surf):
        self.images.append(surf)

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
        self.setpos((self.position[0] + self.speed, self.position[1]))

    def moveleft(self):
        self.setpos((self.position[0] - self.speed, self.position[1]))

    def moveup(self):
        self.setpos((self.position[0], self.position[1] - self.speed))

    def movedown(self):
        self.setpos((self.position[0], self.position[1] + self.speed))
