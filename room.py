import constants
import pygame
import tile
import sys, os

class Room:
    tiles = {}
    width = 0
    height = 0
    board = []
    unwalkable = pygame.sprite.Group()

    def __init__(self, fname):
        state = "init"
        tmptiles = []
        f = open(fname)
        for line in f:
            line = line.rstrip()
            if line == "" or line[0] == '#':
                continue
            if state == "init":
                if line == "HIVE":
                    state = "params"
                else:
                    sys.exit("Malformed room file")
            elif state == "params":
                if line == "Tiles":
                    state = "tiles"
                else:
                    [self.width, self.height] = line.split()
            elif state == "tiles":
                if line == "Map":
                    state = "map"
                else:
                    tmptiles.append(line.split())
            elif state == "map":
                self.board.append(map(int, line.split()))
        for tmp in tmptiles:
            img = pygame.image.load(os.path.join(constants.graphicspath, constants.tilepath, tmp[0]))
            img.convert()
            if int(tmp[2]) == 0:
                self.tiles[int(tmp[1])] = tile.Tile(img, tmp[0], False)
            else:
                self.tiles[int(tmp[1])] = tile.Tile(img, tmp[0], True)

        i = 0
        j = 0
        while i < len(self.board):
            while j < len(self.board[i]):
                self.tiles[self.board[i][j]].addpos((j,i))
                if not self.tiles[self.board[i][j]].walkable:
                    self.unwalkable.add(self.tiles[int(tmp[1])].sprites[-1])
                j += 1
            i += 1
            j = 0


    def draw(self, window):
        for t in self.tiles.values():
            t.draw(window)
