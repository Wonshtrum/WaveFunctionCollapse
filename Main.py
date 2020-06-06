from UI import *
from Editor import *
from TileSet import *

tileSize = 3
displaySet = TileSet(tileSize, 10, 10, 10, 0.1)
editorSet = TileSet(tileSize, 4, 4, 10, 0.5)

editor = Editor(editorSet, displaySet)

editor.picker.loop()
