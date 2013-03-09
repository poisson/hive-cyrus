import constants
import pygame

class Bullet:
    pgsprite = None
    image = None
    position = (10,10)
    destination = (10,10)
    speed = .3

    def draw(self, window):
        window.blit(self.image, (self.position[0]*constants.tilesize, self.position[1]*constants.tilesize))

    def __init__(self, img, player):
        self.pgsprite = pygame.sprite.Sprite()
        self.image = img.copy()
        self.pgsprite.image = img.copy()
        self.pgsprite.rect = pygame.Rect(player.position[0]*constants.tilesize, player.position[1]*constants.tilesize, constants.tilesize, constants.tilesize)
        self.position = (player.position[0], player.position[1])
        if player.direction == 0:
            self.destination = (self.position[0], self.position[1] + 9999)
        elif player.direction == 1:
            self.destination = (self.position[0] - 9999, self.position[1])
        elif player.direction == 2:
            self.destination = (self.position[0], self.position[1] - 9999)
        else:
            self.destination = (self.position[0] + 9999, self.position[1])

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
        if abs(self.position[0] - self.destination[0]) < self.speed:
            self.position = (self.destination[0], self.position[1])
        elif self.position[0] < self.destination[0]:
            self.moveright()
        elif self.position[0] > self.destination[0]:
            self.moveleft()

    def updatey(self):
        if abs(self.position[1] - self.destination[1]) < self.speed:
            self.position = (self.position[0], self.destination[1])
        if self.position[1] < self.destination[1]:
            self.movedown()
        elif self.position[1] > self.destination[1]:
            self.moveup()
