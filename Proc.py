UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Proc:
    def __init__(self, tileSet, links):
        self.tileSet = tileSet
        self.links = links
        self.n = links.n
        self.grid = None
    
    def updateTile(self, tx, ty):
        s = self.tileSet.tileSize
        grid = self.tileSet.grid[tx][ty]
        tiles = self.grid[tx][ty]
        for x in range(s):
            for y in range(s):
                if x*s+y in tiles:
                    grid[x][y] = 9
                else:
                    grid[x][y] = 0

    def updateTiles(self):
        for tx in range(self.tileSet.tileWidth):
            for ty in range(self.tileSet.tileHeight):
                self.updateTile(tx, ty)

    def reset(self):
        self.grid = [[list(range(self.n)) for x in range(self.tileSet.tileWidth)] for y in range(self.tileSet.tileHeight)]
        self.updateTiles()

    def update(self, x, y):
        newList = []
        links = self.links.links
        width = self.tileSet.tileWidth
        height = self.tileSet.tileHeight
        grid = self.grid
        less = False
        for tile in grid[x][y]:
            up = links[tile, UP]
            right = links[tile, RIGHT]
            down = links[tile, DOWN]
            left = links[tile, LEFT]
            valid = all((
                y <= 0 or any(_ in grid[x][y-1] for _ in up),
                x >= width-1 or any(_ in grid[x+1][y] for _ in right),
                y >= height-1 or any(_ in grid[x][y+1] for _ in down),
                x <= 0 or any(_ in grid[x-1][y] for _ in left)))
            if valid:
                newList.append(tile)
            else:
                less = True
        if less:
            grid[x][y] = newList
            self.updateTile(x, y)
            if y > 0:
                self.update(x, y-1)
            if x < width-1:
                self.update(x+1, y)
            if y < height-1:
                self.update(x, y+1)
            if x < 0:
                self.update(x-1, y)

    def ripple(self, x, y):
        width = self.tileSet.tileWidth
        height = self.tileSet.tileHeight
        if y > 0:
            self.update(x, y-1)
        if x < width-1:
            self.update(x+1, y)
        if y < height-1:
            self.update(x, y+1)
        if x < 0:
            self.update(x-1, y)
