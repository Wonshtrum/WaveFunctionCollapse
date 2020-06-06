import tkinter as tk
from sys import exit
from random import randrange
from Part import Links
from Proc import Proc

class View:
    def __init__(self, width = 800, height = 600, **kwargs):
        self.width = width
        self.height = height
        self.win = tk.Tk()
        self.can = tk.Canvas(self.win, width = width+1, height = height+1, **kwargs)
        self.can.pack()
        self.win.protocol("WM_DELETE_WINDOW", exit)

    def loop(self):
        self.win.mainloop()

class Picker:
    def __init__(self, tileSet):
        self.view = View(*tileSet.getViewPort())
        tileSet.apply(self.view)

class Editor:
    def __init__(self, view, tileSet, displaySet):
        self.view = view
        self.tileSet = tileSet
        self.links = Links(tileSet)
        self.display = displaySet
        self.proc = Proc(displaySet, self.links)
        tileSet.apply(view)
        self.can = self.view.can
        self.cursor = self.tileSet.createPixel(0, 0, 0, 0, outline = "red", width = 3)
        self.can.bind("<Motion>", self.move)
        self.can.bind("<1>", self.rightClick)
        self.can.bind("<3>", self.leftClick)

    def move(self, event):
        x, y, inBound = self.tileSet.clamp(event.x, event.y)
        if not(inBound):
            x = y = -self.tileSet.tilePixelSize*2
        self.can.coords(self.cursor, x, y, x+self.tileSet.tilePixelSize, y+self.tileSet.tilePixelSize)

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
        self.display.updateTiles()

    def leftClick(self, event):
        tx, ty, x, y = self.tileSet.pick(event.x, event.y)
        if self.tileSet.bound(tx, ty, x, y):
            tile = tx*self.tileSet.tileHeight+ty
            for d in range(4):
                print(self.links.links[tile, d])
