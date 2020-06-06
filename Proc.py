UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Proc:
    def __init__(self, primSet, tileSet, displaySet, links):
        self.primSet = primSet
        self.tileSet = tileSet
        self.display = displaySet
        self.links = links
        self.n = links.n
        self.grid = None
        self.reset()
    
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
        if len(tiles) == 1:
            x, y = tiles[0]//self.tileSet.tileSize, tiles[0]%self.tileSet.tileSize
            self.display.grid[tx][ty] = self.primSet.grid[x][y]
        else:
            self.display.grid[tx][ty] = self.display.emptyTile

    def updateTiles(self):
        for tx in range(self.tileSet.tileWidth):
            for ty in range(self.tileSet.tileHeight):
                self.updateTile(tx, ty)

    def reset(self, update = False):
        self.grid = [[list(range(self.n)) for x in range(self.tileSet.tileWidth)] for y in range(self.tileSet.tileHeight)]
        self.updateTiles()
        for tx in range(self.display.tileWidth):
            for ty in range(self.display.tileHeight):
                self.display.grid[tx][ty] = self.display.emptyTile
        if update:
            self.update(0, 0)
        self.tileSet.updateTiles()
        self.display.updateTiles()

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
            if x > 0:
                self.update(x-1, y)

    def updateAll(self):
        for tx in range(self.tileSet.tileWidth):
            for ty in range(self.tileSet.tileHeight):
                self.update(tx, ty)

    def ripple(self, x, y):
        width = self.tileSet.tileWidth
        height = self.tileSet.tileHeight
        if y > 0:
            self.update(x, y-1)
        if x < width-1:
            self.update(x+1, y)
        if y < height-1:
            self.update(x, y+1)
        if x > 0:
            self.update(x-1, y)
