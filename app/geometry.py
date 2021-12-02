# Copyright (c) 2011 Cosku Acay, http://www.coskuacay.com

from math import *

"""
THE LIBRARY THAT HANDLES ALL MATH

Most functions in this module assume that you pass a LIST of points.
Unlike Tkinter points, all points must be LISTs of two coordinates (x and y).
Functions directly affect the lists, and generally do not return any variables.
"""

'''/////Transition Functions/////'''


# Rotates and scales a polygon
def rotateScalePolygon(polygon, rad, factor):
    cosine = cos(rad) * factor  # Get cosine
    sine = sin(rad) * factor  # Get sine

    # Note that since all values are lists, we don't need to store them back
    for point in polygon:
        x = point[0] * cosine - point[1] * sine  # Get new x
        y = point[0] * sine + point[1] * cosine  # Get new y
        point[0] = x  # Store back
        point[1] = y
    return


# For re-centering polygons
def addOffset(polygon, offset):
    for point in polygon:
        point[0] += offset[0]
        point[1] += offset[1]
    return  # Note that we don't need to return the list


# /////Calculation Functions/////


# Returns the radius of the bounding circle (distance to farthest point)
def boundingCircle(polygon):
    maxDistance = 0  # Store maximum distance here
    for point in polygon:
        dist = point[0] * point[0] + point[1] * point[1]  # Current distance
        if (dist > maxDistance): maxDistance = dist  # Swap if greater
    return maxDistance ** 0.5  # Return the square root


def Centroid(polygon):
    """
    Returns the centroid of a polygon.

    This function calculates the actual centroid. It calculates the
    area (which is necessary to find the centroid) also.
    Taken from: "http://en.wikipedia.org/wiki/Centroid".
    """
    # This function assumes a closed polygon (point(n)=point(0))
    area = 0.0  # Calculate the area with this
    sumX = 0.0  # Sum of x coordinates
    sumY = 0.0  # Sum of y coordinates
    common = 0.0  # Common term in the equation(s)

    for index in range(len(polygon) - 1):  # Repeat for index up to n-1
        # Calculate the common term (used in three places)
        common = polygon[index][0] * polygon[index + 1][1]
        common -= polygon[index + 1][0] * polygon[index][1]
        area += common  # Add area component
        # Add coordinates
        sumX += (polygon[index][0] + polygon[index + 1][0]) * common
        sumY += (polygon[index][1] + polygon[index + 1][1]) * common
    area *= 3.0  # Simplified version of centroid formula (6 * 0.5)
    return (sumX / area, sumY / area)


# /////Helper Functions/////


# Copies a polygon and returns a list. Solves the "pointer" problem.
def copyPolygon(polygon):
    newList = []
    for point in polygon:
        newList.append(list(point))
    return newList


# Removes the center offset. For re-centering polygons at the beginning.
def removeCenter(polygon, center):
    addOffset(polygon, [-center[0], -center[1]])
