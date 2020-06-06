from UI import *
from TileSet import *

tileSize = 5
displaySet = TileSet(tileSize, 10, 10, 10)
editorSet = TileSet(tileSize, 4, 4, 10, 0.5)

main = View(*displaySet.getViewPort())
editor = Editor(View(*editorSet.getViewPort()), editorSet, displaySet)
displaySet.apply(main)

for i in range(10):
    for j in range(10):
        displaySet.grid[i][j] = editorSet.grid[0][0]

main.loop()
