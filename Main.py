from UI import *
from TileSet import *

tileSize = 3
displaySet = TileSet(4, 10, 10, 10, 0.5)
editorSet = TileSet(tileSize, 4, 4, 10, 0.5)

main = View(*displaySet.getViewPort())
displaySet.apply(main)
editor = Editor(View(*editorSet.getViewPort()), editorSet, displaySet)

main.loop()
