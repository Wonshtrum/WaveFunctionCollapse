import tkinter as tk
from sys import exit
from random import randrange

def color(i):
    return "#"+str(i)*3

def bound(m, x, M):
    return m <= x < M

class TileSet:
    def __init__(self, tileSize, tileWidth, tileHeight, tilePixelSize, spacer = 0, can = None):
        self.tileSize = tileSize
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.tilePixelSize = tilePixelSize
        self.spacer = spacer
        self.can = can
        self.grid = [[[[0]*tileSize for _ in range(tileSize)] for __ in range(tileHeight)] for ___ in range(tileWidth)]
        self.pixels = [[[[0]*tileSize for _ in range(tileSize)] for __ in range(tileHeight)] for ___ in range(tileWidth)]

    def bound(self, tx, ty, x, y):
        return bound(0, tx, self.tileWidth) and bound(0, ty, self.tileHeight) and bound(0, x, self.tileSize) and bound(0, y, self.tileSize)

    def createPixel(self, tx, ty, x, y, **kwargs):
        ox, oy = self.warp(tx, ty, x, y)
        return self.can.create_rectangle(ox, oy, ox+self.tilePixelSize, oy+self.tilePixelSize, **kwargs)

    def apply(self, view):
        self.can = view.can
        for tx in range(self.tileWidth):
            for ty in range(self.tileHeight):
                for x in range(self.tileSize):
                    for y in range(self.tileSize):
                        self.pixels[tx][ty][x][y] = self.createPixel(tx, ty, x, y)

    def updateTile(self, tx, ty):
        for x in range(self.tileSize):
            for y in range(self.tileSize):
                self.can.itemconfig(self.pixels[tx][ty][x][y], fill = color(self.grid[tx][ty][x][y]))
    
    def updateTiles(self):
        for tx in range(self.tileWidth):
            for ty in range(self.tileHeight):
                self.updateTile(tx, ty)

    def pick(self, x, y):
        x = (x-1)/self.tilePixelSize-self.spacer
        y = (y-1)/self.tilePixelSize-self.spacer
        tx = x//(self.tileSize+self.spacer)
        ty = y//(self.tileSize+self.spacer)
        x = int(x-tx*(self.tileSize+self.spacer))
        y = int(y-ty*(self.tileSize+self.spacer))
        return (tx, ty, x, y)

    def warp(self, tx, ty, x, y):
        return (((self.tileSize+self.spacer)*tx+x+self.spacer)*self.tilePixelSize+1,
                ((self.tileSize+self.spacer)*ty+y+self.spacer)*self.tilePixelSize+1)

    def clamp(self, x, y):
        tx, ty, x, y = self.pick(x, y)
        return (*self.warp(tx, ty, x, y), self.bound(tx, ty, x, y))

    def getViewPort(self):
        return (((self.tileSize+self.spacer)*self.tileWidth+self.spacer)*self.tilePixelSize,
                ((self.tileSize+self.spacer)*self.tileHeight+self.spacer)*self.tilePixelSize)

class View:
    def __init__(self, width = 800, height = 600, **kwargs):
        self.width = width
        self.height = height
        self.win = tk.Tk()
        self.can = tk.Canvas(self.win, width = width+1, height = height+1, **kwargs)
        self.can.pack()

    def loop(self):
        self.win.protocol("WM_DELETE_WINDOW", exit)
        self.win.mainloop()

class Editor:
    def __init__(self, view, tileSet):
        self.view = view
        self.tileSet = tileSet
        tileSet.apply(view)
        self.can = self.view.can
        self.cursor = self.tileSet.createPixel(0, 0, 0, 0, outline = "red", width = 3)
        self.can.bind("<Motion>", self.move)
        self.can.bind("<1>", self.click)

    def move(self, event):
        x, y, inBound = self.tileSet.clamp(event.x, event.y)
        if not(inBound):
            x = y = -self.tileSet.tilePixelSize*2
        self.can.coords(self.cursor, x, y, x+self.tileSet.tilePixelSize, y+self.tileSet.tilePixelSize)

    def click(self, event):
        for tx in range(self.tileSet.tileWidth):
            for ty in range(self.tileSet.tileHeight):
                for x in range(self.tileSet.tileSize):
                    for y in range(self.tileSet.tileSize):
                        self.tileSet.grid[tx][ty][x][y] = randrange(10)
                self.tileSet.updateTile(tx, ty)
        displaySet.updateTiles()

tileSize = 5
displaySet = TileSet(tileSize, 10, 10, 10)
editorSet = TileSet(tileSize, 4, 4, 10, 0.5)

main = View(*displaySet.getViewPort())
editor = Editor(View(*editorSet.getViewPort()), editorSet)
displaySet.apply(main)
for i in range(10):
    for j in range(10):
        displaySet.grid[i][j] = editorSet.grid[0][0]

main.loop()
