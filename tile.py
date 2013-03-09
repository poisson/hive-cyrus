import constants
import pygame

class Tile:
    surface = None
    sprites = []
    positions = []
    fname = ""
    walkable = True

    def __init__(self, surf, fname, walk=False, pos=None):
        self.surface = surf
        self.fname = fname
        if pos != None:
            self.addpos(pos)
        else:
            self.positions = []
        self.walkable = walk

    def addpos(self, pos):
        self.positions.append(pos)
        self.sprites.append(pygame.sprite.Sprite())
        self.sprites[-1].rect = (pos[0]*constants.tilesize, pos[1]*constants.tilesize, constants.tilesize, constants.tilesize)

    def draw(self, window):
        for p in self.positions:
            window.blit(self.surface, (p[0]*constants.tilesize, p[1]*constants.tilesize))
