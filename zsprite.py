import constants
import pygame

class zSprite:
    pgsprite = None
    images = []
    frame = 0
    position = (10,10)
    destination = (10,10)
    speed = .15
    backoff = []
    counter = 0

    def clone(self):
        cl = zSprite(self.images[0], self.position)
        cl.images = list(self.images)
        cl.frame = self.frame
        cl.destination = (self.destination[0], self.destination[1])
        cl.counter = self.counter
        return cl

    def draw(self, window):
        window.blit(self.images[self.frame], (self.position[0]*constants.tilesize, self.position[1]*constants.tilesize))
        self.counter += 1
        if self.counter >= 5:
            self.frame += 1
            self.counter = 0
            if (self.frame % len(self.images)) == 0:
                self.frame = 0

    def __init__(self, img, pos=(10,10)):
        self.pgsprite = pygame.sprite.Sprite()
        self.images = [img.copy()]
        self.pgsprite.image = img.copy()
        self.pgsprite.rect = pygame.Rect(pos[0]*constants.tilesize, pos[1]*constants.tilesize, constants.tilesize, constants.tilesize)
        self.position = (pos[0], pos[1])
        self.frame = 0

    def addimg(self, surf):
        self.images.append(surf.copy())

    def setpos(self, pos):
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

    def updatex(self):
        self.backoff = []
        if abs(self.position[0] - self.destination[0]) < self.speed:
            self.position = (self.destination[0], self.position[1])
        elif self.position[0] < self.destination[0]:
            self.moveright()
            self.backoff.append(self.moveleft)
        elif self.position[0] > self.destination[0]:
            self.moveleft()
            self.backoff.append(self.moveright)

    def updatey(self):
        self.backoff = []
        if abs(self.position[1] - self.destination[1]) < self.speed:
            self.position = (self.position[0], self.destination[1])
        if self.position[1] < self.destination[1]:
            self.movedown()
            self.backoff.append(self.moveup)
        elif self.position[1] > self.destination[1]:
            self.moveup()
            self.backoff.append(self.movedown)
