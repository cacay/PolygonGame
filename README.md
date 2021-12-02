Polygon Game v1.8
================================
Polygon Game is an asteroids game I developed in Python for a CS course I took
during summer at CMU. I had made a similar game on GameMaker before to get
practice working with controllers. This time, I did not want to use images I
found online and wanted to write the game engine myself, so I used polygons for
all graphical content. My code handles all operations on vectors (scaling,
rotations etc.) and uses the separating plane method
(
see [here](http://www.codeproject.com/Articles/15573/2D-Polygon-Collision-Detection))
for exact polygon collision detection. I had only a week to complete the
project, but I think it turned out to be quite fun. I improved on it a little
afterwards and thus the version 1.8.

How to Run
--------------------------------

1. Install Python 3 if you do not have it already. Most Linux distributions
   already come with Python. If you are using Windows or Mac, you may need
   to [download] (http://www.python.org/download/) it.
2. Install TkInter. This is the de-facto GUI package for Python and usually
   comes bundled up with it. Some Linux distributions may not have it by
   default; just search it online if that is the case.
3. Finally, run `__main__.py`.

Instructions
--------------------------------
The red isosceles triangle that starts in the middle of the screen is your ship.
Your goal is to avoid all asteroids and shoot them down. Every object except for
bullets wrap around the screen. You only have one life so use it well.

### Controls

* Arrow keys to move around (down arrow slows you down instead of going
  backwards)
* Space to shoot
* P to pause
* G to toggle god mode (note: you cannot kill enemies if they are colliding with
  you)
* Enter to spawn an octagon (for debugging purposes and because octagons are
  cool)

Files
--------------------------------

* `main.py`: This is where all the game code is.
* `gui.py`: Handles all the GUI stuff.
* `collisions.py`: All the code required to check for polygon collisions.
* `geometry.py`: This is like a vector math library.
* `smart.py`: Contains the “smartObject” and “bullet” classes. These can draw
  themselves, check for collisions and more.
* `data.py`: Contains polygon point data and some functions to generate them.
* `create.py`: Helper functions that create enemy objects (for handling levels).
* `generators.py`: Helper functions to quickly generate base objects.
 