# Copyright (c) 2011 Cosku Acay, http://www.coskuacay.com

from math import *
from geometry import *
import collisions

# THIS IS THE SMART OBJECTS CLASS

# Global variables
wrapOffset = 5  # Pixels to wait before wrapping
display = [0, 0, 1]

'''
These classes do much of the calculations automatically, are highly portable
and convinient to use.
'''


# Scales a list of two integers
def scalePos(position, factor):
    return [position[0] * factor, position[1] * factor]


# Smart Object Class
class smartObject:
    # Object initializer
    def __init__(self, shape, canvas):
        self.data = {}  # To store arbitrary data
        self.canvas = canvas  # The canvas to store things in
        self.hidden = False  # Hidden objects are not displayed
        self.wraps = True  # Will automatically wrapsAround

        self.shape = shape  # Shape data
        self.scale = 1.0  # Scaling amount (size)

        self.position = [0.0, 0.0]  # Current position
        self.speed = 0.0  # Speed of the object
        self.direction = 0.0  # Current direction (pointing left)
        self.rotation = 0.0  # Rotation around center (left)
        self.angularSpeed = 0.0  # Rotating speed

        self.health = 1  # Remaining health

    # Creates a copy of itself and returns it
    def duplicate(self):
        new = smartObject(self.shape, self.canvas)
        new.data = dict(self.data)

        new.scale = self.scale
        new.position = list(self.position)
        new.speed = self.speed
        new.direction = self.direction
        new.rotation = self.rotation
        new.angularSpeed = self.angularSpeed

        new.health = self.health
        return new

    # Moves the object
    def step(self):
        # Move according to speed and direction
        speedX = self.speed * cos(self.direction)  # X component
        speedY = self.speed * sin(self.direction)  # Y component
        self.position[0] += speedX
        self.position[1] += speedY
        if self.wraps == True: self.wrapAround()

        # Add angularSpeed
        self.rotation += self.angularSpeed
        if self.rotation >= 2 * pi: self.rotation -= 2 * pi
        if self.rotation < 0: self.rotation += 2 * pi

    # Draws itself on the canvas
    def draw(self):
        # Get a new polygon and apply all transitions
        self.tempPoly = copyPolygon(self.shape.polygon)  # Get a new copy
        # Rotate polygon
        rotateScalePolygon(self.tempPoly, self.rotation, self.scale * display[2])
        # Move to the correct position on screen
        addOffset(self.tempPoly, scalePos(self.position, display[2]))

        # Don't draw the last point
        if self.hidden == False:
            self.canvas.create_polygon(self.tempPoly[:-1], fill=self.shape.fill,
                                       outline=self.shape.outline,
                                       width=self.shape.width)
        return

    # Checks if object collides a smart object
    def collidesObject(self, smartObject):
        bounding1 = self.shape.boundingR * self.scale
        bounding2 = smartObject.shape.boundingR * smartObject.scale
        if not (collisions.circlesCollide(self.position, bounding1,
                                          smartObject.position, bounding2)):
            return False
        return collisions.polygonsCollide(self.tempPoly, smartObject.tempPoly)

    # Checks if object collides a circle
    def collidesBullet(self, bullet):
        bounding1 = self.shape.boundingR * self.scale
        if not (collisions.circlesCollide(self.position, bounding1,
                                          bullet.position, bullet.size)):
            return False
        return collisions.circPolyCollide(self.tempPoly,
                                          scalePos(bullet.position, display[2]), bullet.size * display[2])

    # Wraps around if it is outside the game screen
    def wrapAround(self):
        global wrapOffset
        radius = self.shape.boundingR * self.scale  # Bounding circle radius
        # Left
        if self.position[0] + radius + wrapOffset < 0:
            if (self.direction > pi / 2) and (self.direction < 1.5 * pi):
                self.position[0] = display[0] + radius
        # Up
        if self.position[1] + radius + wrapOffset < 0:
            if (self.direction > pi):
                self.position[1] = display[1] + radius
        # Right
        if self.position[0] - radius - wrapOffset > display[0]:
            if (self.direction < pi / 2) or (self.direction > 1.5 * pi):
                self.position[0] = -radius
        # Down
        if self.position[1] - radius - wrapOffset > display[1]:
            if (self.direction < pi):
                self.position[1] = -radius


# Bullet class, for creating bullets...
class bullet:
    def __init__(self, canvas, fill, outline, width, size, speed, life):
        self.canvas = canvas
        self.fill = fill
        self.outline = outline
        self.width = width
        self.size = size
        self.position = [0, 0]
        self.speed = speed
        self.direction = 0
        self.life = life

    # Creates a copy of itself and returns it
    def duplicate(self):
        new = bullet(self.canvas, self.fill, self.outline, self.width,
                     self.size, self.speed, self.life)
        new.position = list(self.position)
        new.speed = self.speed
        new.direction = self.direction
        return new

    # Moves the bullet
    def step(self):
        # Move according to speed and direction
        self.position[0] += self.speed * cos(self.direction)  # X component
        self.position[1] += self.speed * sin(self.direction)  # Y component

    # Draws itself on the canvas
    def draw(self):
        x = self.position[0] * display[2]
        y = self.position[1] * display[2]
        r = self.size / 2 * display[2]
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.fill,
                                outline=self.outline, width=self.width)
        return

    # Checks if the bullet is outside of game screen
    def outside(self):
        global wrapOffset
        x = self.position[0]
        y = self.position[1]
        radius = self.size

        if (x + radius + wrapOffset < 0) or (y + radius + wrapOffset < 0) or \
                (x - radius - wrapOffset > display[0]) or \
                (y - radius - wrapOffset > display[1]):
            return True
        return False


# Shape class contains information such as polygon data, color, outline...
class shape:
    # Changes the polygon
    def changePolygon(self, polygon, center):
        # The last point must be the same with the first one
        if polygon[-1] <> polygon[0]:
            polygon.append(list(polygon[0]))

        self.polygon = polygon
        # Calculate the center
        if tuple(center) == (0, 0) or center == "":
            return
        elif center == "CENTROID":
            newCenter = Centroid(polygon)
        elif center == "CENTER":
            newCenter = Center(polygon)
        else:
            newCenter = tuple(center)

        # Even though newCenter is first used inside a conditional
        # it will always be defined here
        removeCenter(polygon, newCenter)  # Remove the center

    # Changes the bounding circle radius
    def changeBounding(self, polygon, radius):
        if radius == "CALC":  # We need to calculate it
            self.boundingR = boundingCircle(polygon)
        else:
            self.boundingR = radius

    # Object initializer
    def __init__(self, polygon, center, fill, outline, width, radius):
        # Change polygon
        self.changePolygon(polygon, center)

        # Initialize other variables
        self.fill = fill  # Fill color
        self.outline = outline  # Outline color
        self.width = width  # Outline width

        # Changes the bounding circle radius
        self.changeBounding(polygon, radius)

    # Creates a copy of itself and returns it
    def duplicate(self):
        new = shape(self.polygon, (0, 0), self.fill, self.outline,
                    self.width, self.boundingR)
        return new
