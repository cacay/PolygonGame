Polygon Game v1.8
================================
Polygon Game is an asteroids game I developed in Python for a CS course I took during summer at CMU. I had made a similar game on GameMaker before to get practice working with controllers. This time, I did not want to use images I found online and wanted to write the game engine myself, so I used polygons for all graphical content. My code handles all operations on vectors (scaling, rotations etc.) and uses the separating plane method (see [here] (http://www.codeproject.com/Articles/15573/2D-Polygon-Collision-Detection)) for exact polygon collision detection. I had only a week to complete the project, but I think it turned out to be quite fun. I improved on it a little afterwards and thus the version 1.8.

How to Run
--------------------------------
1.  Install Python if you do not have it already. Most Linux distributions already come with Python. If you are using Windows or Mac, you may need to [download] (http://www.python.org/download/) it. Python is a great scripting language and it certainly is worth installing even if it is not for this game.
2.  Install TkInter. This is the de-facto standard GUI package for Python and usually comes bundled up with it. Some Linux distributions may not have it by default; just search it online if that is the case.
3.  Finally, run “Run.pyw.” This could involve either double-clicking the file (Windows and Mac) or typing `python Run.pyw` in the command line (Linux).

Instructions
--------------------------------
The red isosceles triangle that starts in the middle of the screen is your ship. Your goal is to avoid all asteroids and shoot them down. You only have one life so use it well.
###Controls
* Arrow keys to move around (down arrow slows you down instead of going backwards)
* Space to shoot
* P to pause
* G to toggle god mode (note: you cannot kill enemies if they are colliding with you)
* Enter to spawn an octagon (for debugging purposes and because octagons are cool)

Files
--------------------------------
* `Run.pyw`: Just runs the game, nothing special.
* `main.py`: This is where all the game code is.
* `gui.py`: Handles all the GUI stuff.
* `collisions.py`: All the code required to check for polygon collisions.
* `geometry.py`: This is like a vector math library.
* `smart.py`: Contains the “smartObject” and “bullet” classes. These can draw themselves, check for collisions and more.
* `data.py`: Contains polygon point data and some functions to generate them.
* `create.py`: Helper functions that create enemy objects (for handling levels).
* `generators.py`: Helper functions to quickly generate base objects.

License
--------------------------------
This code is distributed under the MIT License, which is reproduced below and in the `LICENSE` file. You can do whatever you want with the code, but I will not be liable for ANY kind of damage that this code might cause. 

Copyright (c) 2011 Cosku Acay, http://www.coskuacay.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Contact Me
--------------------------------
You can contact me for any type of questions, suggestions, or bug reports. Either email me at coskuacay@gmail.com or visit my [website] (http://www.coskuacay.com) for more information.

