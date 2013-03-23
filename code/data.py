# Copyright (c) 2011 Cosku Acay, http://www.coskuacay.com

from math import *
from smart import shape
#THIS FILE CONTAINS THE POLYGON DATA

'''Special thanks to GeoGebra'''

#These shapes mostly have unit sizes (width and height of 1)
triangle = [[0,-0.4],[sqrt(3)/2.0, 0],[0,0.4]]
rightTri = [[0,0],[1,0],[0,1]]
#A triangle from a pentagon
pentri = [[0,0], [sqrt(2-2*cos(radians(108))),0],[cos(radians(36)),
                                                sin(radians(36))]]

#Creates a regular polygon and returns it
def createRegular(sides):
    angle = 2*pi/sides
    currentAngle = 0.0
    newPolygon = [[0,0]]
    for index in xrange(sides-1):
        currentAngle += angle
        newPoint = [newPolygon[index][0]+cos(currentAngle),
                        newPolygon[index][1]+sin(currentAngle)]
        newPolygon.append(newPoint)
    return newPolygon

#Pentagon shrinks when attacked. This function creates all steps
def createPentagons(fill, outline, width):
    global pentagons

    temp = list(createRegular(5))
    pentagons=[]
    #Step 2
    temp.pop(1)
    pentagons.append(shape(list(temp),"CENTROID", fill, outline, width, "CALC"))
    #Step 3
    temp.pop(3)
    pentagons.insert(0,shape(list(temp),"CENTROID", fill, outline, width, "CALC"))

    return pentagons
