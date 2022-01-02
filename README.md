# easytile_blender
Dead simple, barebones Blender (2.83) addon for placing meshes as tiles.

## Installation
In Blender, go to Edit > Preferences > Add-ons > Install..., then find the `__init__.py` file of this addon and install it.

## Usage
Adds an 'EasyTile' menu to the sidebar in object mode.

Add tiles to the tile menu by pressing the plus while the object is selected.

Press the 'draw tiles' button (or CTRL-SHIFT-T) to enter tile drawing mode. The currently selected tile can be painted on a flat plane in the 3D view now. Use plus/minus keys to change the grid size. Press ESC at any time to exit tile drawing mode.

ALT + Scroll wheel changes the height of the flat plane, and ALT and plus/minus keys change the increment of the height changes (from scroll wheel).

Tile instances are linked duplicates of the original tile object, so changes to that object will affect all of the instantiated tiles.

Tiles are stored in a collection in the scene called 'EasyTileTiles'.