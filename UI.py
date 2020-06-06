import tkinter as tk
from sys import exit

class View:
    def __init__(self, title, width = 800, height = 600, **kwargs):
        self.width = width
        self.height = height
        self.win = tk.Tk()
        self.win.title(title)
        self.can = tk.Canvas(self.win, width = width+1, height = height+1, **kwargs)
        self.can.pack()
        self.win.protocol("WM_DELETE_WINDOW", exit)

    def loop(self):
        self.win.mainloop()

class Picker(View):
    def __init__(self, title, tileSet):
        super().__init__(title, *tileSet.getViewPort())
        self.tileSet = tileSet
        tileSet.apply(self)
        self.cursor = self.tileSet.createPixel(0, 0, 0, 0, outline = "red", width = 3)
        self.can.bind("<Motion>", self.move)
        self.can.bind("<1>", self.rightClick)
        self.can.bind("<3>", self.leftClick)
        self.mvCallbacks = [self.mvDefault]
        self.rcCallbacks = []
        self.lcCallbacks = []

    def mvDefault(self, event):
        x, y, inBound = self.tileSet.clamp(event.x, event.y)
        if not(inBound):
            x = y = -self.tileSet.tilePixelSize*2
        self.can.coords(self.cursor, x, y, x+self.tileSet.tilePixelSize, y+self.tileSet.tilePixelSize)

    def move(self, event):
        for cb in self.mvCallbacks:
            cb(event)

    def rightClick(self, event):
        for cb in self.rcCallbacks:
            cb(event)

    def leftClick(self, event):
        for cb in self.lcCallbacks:
            cb(event)
