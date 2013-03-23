# Copyright (c) 2011 Cosku Acay, http://www.coskuacay.com

import random
from smart import *
#THESE ARE THE GENERATORS THAT EASE THINS UP A LITTLE

#This is for creating identical bullets
def bulletGenerator(canvas, fill, outline, width, size, speed):
    #Create a bullet so that you can duplicate() it
    duplicator = bullet(canvas, fill, outline, width, size, speed, 5000/60)

    while True:
        newBullet = duplicator.duplicate()
        #newBullet.step()
        yield newBullet

#This is for creating smartObjects with the same shape
def objectGenerator(canvas, polygon, fill, outline, width, options):
    #If a center to the polygon is given, use it
    if options.has_key("center"):
        center = options["center"]
    else:
        center = "CENTROID"

    #Create the shape object
    newShape = shape(polygon, center, fill, outline, width, "CALC")

    #Original option values, final ones may change due to randomizations
    health = 1
    scale = 1.0
    speed = 0.0
    direction = 0.0
    rotation = 0.0
    angularSpeed = 0.0
    randomScale = 0.0       #Multiply scale by this amount for randomness

    #Get all the options from the given dictionary
    if len(options) <> 0:
        if options.has_key("health"): health=options["health"]
        if options.has_key("scale"): scale=options["scale"]
        if options.has_key("speed"): speed=options["speed"]
        if options.has_key("direction"): direction=options["direction"]
        if options.has_key("rotation"): rotation=options["rotation"]
        if options.has_key("angularSpeed"): angularSpeed=options["angularSpeed"]
        if options.has_key("randomScale"): randomScale=options["randomScale"]

    #Create a smartObject so that you can duplicate() it
    duplicator = smartObject(newShape, canvas)
    duplicator.health = health
    duplicator.speed = speed
    duplicator.angularSpeed = angularSpeed

    #Infinite loop
    while True:
        #Apply randomizations
        newScale = scale * (1 + (random.random()-0.5)*2*randomScale)
        newDirection = direction
        if direction == "RANDOM":
            newDirection = random.random()*2*pi
        newRotation = rotation
        if rotation == "RANDOM":
            newRotation = random.random()*2*pi

        #Create the object and assign values
        newObject = duplicator.duplicate()
        newObject.direction = newDirection
        newObject.rotation = newRotation
        newObject.scale = newScale

        yield newObject     #Return the object
