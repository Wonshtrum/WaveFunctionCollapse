from UI import Picker, View
from random import randrange
from Part import Links
from Proc import Proc
from TileSet import TileSet

class Editor:
    def __init__(self, tileSet, displaySet):
        self.tileSet = tileSet
        self.links = Links(tileSet)
        self.picker = Picker("Editor", tileSet)
        self.picker.rcCallbacks.append(self.rightClick)
        self.picker.lcCallbacks.append(self.leftClick)
        self.helperSet = TileSet(tileSet.tileWidth, displaySet.tileWidth, displaySet.tileHeight, tileSet.tilePixelSize, tileSet.spacer)
        self.helperPicker = Picker("Preview", self.helperSet)
        self.helperPicker.rcCallbacks.append(self.setOnHelper)
        self.proc = Proc(self.helperSet, self.links)
        self.display = displaySet
        self.displayView = View("Result", *displaySet.getViewPort())
        displaySet.apply(self.displayView)

    def rightClick(self, event):
        for tx in range(self.tileSet.tileWidth):
            for ty in range(self.tileSet.tileHeight):
                for x in range(self.tileSet.tileSize):
                    for y in range(self.tileSet.tileSize):
                        self.tileSet.grid[tx][ty][x][y] = randrange(2)*9
                self.tileSet.updateTile(tx, ty)
        self.links.update()
        self.proc.reset()
        self.proc.update(0, 0)
        self.helperSet.updateTiles()

    def leftClick(self, event):
        tx, ty, x, y = self.tileSet.pick(event.x, event.y)
        if self.tileSet.bound(tx, ty, x, y):
            tile = tx*self.tileSet.tileHeight+ty
            for d in range(4):
                print(self.links.links[tile, d])

    def setOnHelper(self, event):
        tx, ty, x, y = self.helperSet.pick(event.x, event.y)
        if self.helperSet.bound(tx, ty, x, y):
            tile = x*self.helperSet.tileSize+y
            active = tile in self.proc.grid[tx][ty]
            print(active)
            if active:
                self.proc.grid[tx][ty].remove(tile)
                self.proc.updateTile(tx, ty)
                self.proc.ripple(tx, ty)
                self.helperSet.updateTiles()
