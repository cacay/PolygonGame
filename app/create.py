# Copyright (c) 2011 Cosku Acay, http://www.coskuacay.com

import app.data as data
from app.generators import *

# THIS CREATES THE ENEMY OBJECTS

# Globals
canvas = 0
MyShip = {}
enemies = {}
generators = {}


# Initialize generators and objects
def init(gameCanvas):
    global MyShip
    global generators
    global canvas
    global polygonShapes

    canvas = gameCanvas
    # Create polygon data
    polygonShapes = data.createPentagons("grey", "black", 1)

    # Create generators
    generators["bulletGen"] = bulletGenerator(canvas, "orange", "black", 2, 8, 25)
    generators["squareGen"] = objectGenerator(canvas, data.createRegular(4), "blue",
                                              "black", 1, {"health": 2, "scale": 55, "direction": "RANDOM",
                                                           "rotation": "RANDOM", "randomScale": 0.15})
    generators["triangleGen"] = objectGenerator(canvas, data.rightTri, "yellow", "black",
                                                1, {"health": 1, "scale": 40, "direction": "RANDOM",
                                                    "rotation": "RANDOM", "randomScale": 0.12})
    generators["pentriGen"] = objectGenerator(canvas, data.pentri, "grey", "black",
                                              1, {"health": 1, "scale": 55, "direction": "RANDOM",
                                                  "rotation": "RANDOM", "randomScale": 0.12})
    generators["pentagonGen"] = objectGenerator(canvas, data.createRegular(5), "grey", "black",
                                                1, {"health": 3, "scale": 55, "direction": "RANDOM",
                                                    "rotation": "RANDOM", "randomScale": 0.12})
    generators["hexegonGen"] = objectGenerator(canvas, data.createRegular(6), "pink", "black",
                                               1, {"health": 6, "scale": 60, "direction": "RANDOM",
                                                   "rotation": "RANDOM", "randomScale": 0.08})
    generators["myGodGen"] = objectGenerator(canvas, data.createRegular(8), "black", "black",
                                             1, {"health": 20, "scale": 12, "direction": "RANDOM",
                                                 "rotation": "RANDOM", "randomScale": 0.08})

    # Create player ship
    newShape = shape(data.triangle, "CENTROID", "brown", "black", 1, "CALC")
    shipObj = smartObject(newShape, canvas)
    shipObj.scale = 50
    MyShip["object"] = shipObj  # smartObject


# Creates a triangle at the given location
def createTriangle(center):
    global generators
    global enemies

    newTriangle = next(generators["triangleGen"])
    newTriangle.position = list(center)
    newTriangle.speed = 4 + random.random() * 8
    newTriangle.angularSpeed = radians(0.01 + random.random() * 10)
    enemies["triangles"].append(newTriangle)


# Pentagons divide when hit. This function handles that
def createPenTri(center):
    global generators
    global enemies

    newTriangle = next(generators["pentriGen"])
    newTriangle.position = list(center)
    newTriangle.speed = 5 + random.random() * 7
    newTriangle.angularSpeed = radians(0.5 + random.random() * 10)
    enemies["triangles"].append(newTriangle)


# Creates a square at a random position
def createRandomSquare():
    global generators
    global enemies

    newSquare = next(generators["squareGen"])
    x = -random.random() * 200
    y = -random.random() * 200
    newSquare.position = [x, y]
    newSquare.speed = 2.5 + random.random() * 7
    newSquare.angularSpeed = radians(0.01 + random.random() * 5)
    enemies["squares"].append(newSquare)


# Creates a pentagon at a random position
def createRandomPentagon():
    global generators
    global enemies

    newPent = next(generators["pentagonGen"])
    x = -random.random() * 200
    y = -random.random() * 200
    newPent.position = [x, y]
    newPent.speed = 3 + random.random() * 5
    newPent.angularSpeed = radians(0.01 + random.random() * 4)
    enemies["pentagons"].append(newPent)


# Creates a hexegon at a random position
def createRandomHexegon():
    global generators
    global enemies

    newHexe = next(generators["hexegonGen"])
    x = -random.random() * 200
    y = -random.random() * 200
    newHexe.position = [x, y]
    newHexe.speed = 2 + random.random() * 4
    newHexe.angularSpeed = radians(0.01 + random.random() * 4)
    enemies["hexegons"].append(newHexe)


# Creates a myGod at a random position
def createRandomMyGod():
    global generators
    global enemies

    newGod = next(generators["myGodGen"])
    x = -random.random() * 200
    y = -random.random() * 200
    newGod.position = [x, y]
    newGod.speed = 15 + random.random() * 6
    newGod.angularSpeed = radians(6 + random.random() * 6)
    enemies["myGod"].append(newGod)
