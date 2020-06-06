from TileSet import TileSet

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def link(tileA, tileB, tileSize, d):
    if d == UP:
        return all(tileA[x][0] == tileB[x][tileSize-1] for x in range(tileSize))
    elif d == DOWN:
        return all(tileA[x][tileSize-1] == tileB[x][0] for x in range(tileSize))
    elif d == RIGHT:
        return all(tileA[tileSize-1][y] == tileB[0][y] for y in range(tileSize))
    elif d == LEFT:
        return all(tileA[0][y] == tileB[tileSize-1][y] for y in range(tileSize))
    else:
        return False

class Links:
    def __init__(self, tileSet):
        self.tileSet = tileSet
        self.n = tileSet.tileWidth*tileSet.tileHeight
        self.tileList = [tileSet.grid[tx][ty] for tx in range(tileSet.tileWidth) for ty in range(tileSet.tileHeight)]
        self.links = {}
        self.update()

    def update(self):
        self.links = {(tile, d): [] for tile in range(len(self.tileList)) for d in range(4)}
        ts = self.tileSet.tileSize
        for a, tileA in enumerate(self.tileList):
            for b, tileB in enumerate(self.tileList):
                for d in (UP, RIGHT):
                    if link(tileA, tileB, ts, d):
                        self.links[a, d].append(b)
                        self.links[b, (d+2)%4].append(a)
