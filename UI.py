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
        self.mvCallbacks = [self.mvDefault]
        self.rcCallbacks = []
        self.mcCallbacks = []
        self.lcCallbacks = []
        self.can.bind("<Motion>", lambda event: self.propagate(event, self.mvCallbacks))
        self.can.bind("<1>", lambda event: self.propagate(event, self.rcCallbacks))
        self.can.bind("<2>", lambda event: self.propagate(event, self.mcCallbacks))
        self.can.bind("<3>", lambda event: self.propagate(event, self.lcCallbacks))

    def propagate(self, event, callbacks):
        for callback in callbacks:
            callback(event)

    def mvDefault(self, event):
        x, y, inBound = self.tileSet.clamp(event.x, event.y)
        if not(inBound):
            x = y = -self.tileSet.tilePixelSize*2
        self.can.coords(self.cursor, x, y, x+self.tileSet.tilePixelSize, y+self.tileSet.tilePixelSize)
