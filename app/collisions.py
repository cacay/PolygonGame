# Copyright (c) 2011 Cosku Acay, http://www.coskuacay.com

from math import *

# THIS MODULE HANDLES ALL COLLISION CALCULATIONS

# /////Circle Collisions/////
'''
These functions check if bounding circles of the polygons overlap or not.
This way calculations can be done much faster.
'''


# Returns the distance between two points without taking the square root
def partialDistance(point1, point2):
    x = point2[0] - point1[0]
    y = point2[1] - point1[1]
    return x * x + y * y


# Returns True if circles intersect each other(a*a + b*b = c*c)
def circlesCollide(center1, r1, center2, r2):
    dist = partialDistance(center1, center2)  # Distance between centers
    c = r1 + r2  # Max distance to collide
    return (c * c >= dist)


# Returns the vertex in polygon closest to center
def closestVertex(polygon, center):
    minDistance = partialDistance(polygon[0], center)  # Closest distance
    minPoint = polygon[0]  # Closest point
    for point in polygon:
        # This is repetitive but this "for" works faster than xrange
        currentDistance = partialDistance(point, center)
        # Change minimum if this is closer
        # No need to use an index for minPoint since it is a pointer
        if currentDistance < minDistance:
            minDistance = currentDistance
            minPoint = point
    return tuple(minPoint)  # Return a copy


# Returns True if a circle and a polygon are overlapping
def circPolyCollide(polygon, center, r):
    # This is based on the SAT algorithm below
    axis = closestVertex(polygon, center)  # Axis is the closest vertex
    circlePro = dotProduct(center, axis)  # Projection of the circle

    test1 = projectPolygon(polygon, axis)  # Min, Max values for poly
    test2 = (circlePro - r, circlePro + r)  # Min, Max values for circle
    return linesOverlap(test1, test2)  # Return collision status


# Normalizes a vector (makes its length 1)
def normalize(vector):
    # Length = sqrt(x*x + y*y)
    magnitude = (vector[0] * vector[0] + vector[1] * vector[1]) ** 0.5
    return (vector[0] / magnitude, vector[1] / magnitude)


# /////Separating Axis Theorem/////
'''
This algorithm can determine whether two CONVEX polygons are colliding
or not. You basically try to find a line that separates the two polygons.
They overlap if you cannot find such a line.
'''


# Returns the dot product of two vectors
def dotProduct(vector1, vector2):
    x = vector1[0] * vector2[0]  # Get x component
    y = vector1[1] * vector2[1]  # Get y component
    return (x + y)


# Returns a normal to a line (a vector perpendicular to a line)
def getNormal(point1, point2):
    # Normal = [-(y2-y1),(x2-x1)]
    x = point1[1] - point2[1]  # Get x component
    y = point2[0] - point1[0]  # Get y component
    return (x, y)


# Projects a polygon on an axis and returns the MIN and MAX values
def projectPolygon(polygon, axis):
    # Initialize Min and Max to some value
    product = dotProduct(polygon[0], axis)  # Project the first point
    Min = Max = product  # Non-capitalized names are reserved

    # Project each vertex of the polygon on the axis
    for point in polygon:
        # I repeat it for the first point for efficiency reasons.
        # The last point is also the same, so it is unnecessary too.
        # However, this "for" works faster than xrange.
        product = dotProduct(point, axis)
        if (product <= Min):
            Min = product
        elif (product > Max):
            Max = product
    return (Min, Max)


# Returns True if two polygons are intersecting
def polygonsCollide(poly1, poly2):
    # Assumes a closed polygon (vertex(n) = vertex(0))

    # Check for each edge of the first polygon
    for index in xrange(len(poly1) - 1):
        normal = getNormal(poly1[index], poly1[index + 1])  # Get the normal
        test1 = projectPolygon(poly1, normal)  # Min, Max values for poly1
        test2 = projectPolygon(poly2, normal)  # Min, Max values for poly2
        # If lines are not intersecting, polygons are separated
        if linesOverlap(test1, test2) == False: return False

    # Repeat the same thing for the other polygon
    for index in xrange(len(poly2) - 1):
        normal = getNormal(poly2[index], poly2[index + 1])  # Get the normal
        test1 = projectPolygon(poly1, normal)  # Min-Max values for poly1
        test2 = projectPolygon(poly2, normal)  # Min-Max values for poly2
        # If lines are not intersecting, polygons are separated
        if linesOverlap(test1, test2) == False: return False

    # If all tests fail, polygons are overlapping
    return True


# Returns True if two lines intersect in 1D
def linesOverlap(line1, line2):
    # Remove the "offset", lines intersect if the new value is less than 0
    dist1 = line1[0] - line2[1]  # Get Min1 - Max2
    dist2 = line2[0] - line1[1]  # Get Min2 - Max1
    return (dist1 <= 0) and (dist2 <= 0)  # Return True if they overlap
