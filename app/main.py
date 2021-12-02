# Copyright (c) 2011 Cosku Acay, http://www.coskuacay.com

import create
from create import *


# THIS IS THE MAIN GAME FILE

# Goes through all objects, moves them and calculates interactions
def stepAll():
    global MyShip
    enemies = create.enemies

    # Move myShip
    MyShip["object"].step()

    # Move bullets
    tempList = MyShip["bullets"]
    for bullet in tempList:
        bullet.step()
        bullet.life -= 1
        if bullet.outside() or bullet.life <= 0:
            tempList.remove(bullet)

    # Move enemy objects
    tempList = enemies["squares"]
    for enemy in tempList:
        enemy.step()

    tempList = enemies["triangles"]
    for enemy in tempList:
        enemy.step()

    tempList = enemies["pentagons"]
    for enemy in tempList:
        enemy.step()

    tempList = enemies["hexegons"]
    for enemy in tempList:
        enemy.step()

    # Move MyGod particles then gravityPull everything
    tempList = enemies["myGod"]
    for enemy in tempList:
        enemy.step()

    for enemy in tempList:
        gravityPull(enemy.position, 2, 1, 5)


# Gravity effect for MyGod particles
def gravityPull(sourcePos, strObjects, strMyShip, strBullets):
    global MyShip
    enemies = create.enemies

    # Pull MyShip
    MyShip["object"].position = pull(sourcePos, MyShip["object"].position, strMyShip)

    # Pull Bullets
    tempList = MyShip["bullets"]
    for bullet in tempList:
        bullet.position = pull(sourcePos, bullet.position, strBullets)

    # Pull enemy objects
    tempList = enemies["squares"]
    for enemy in tempList:
        enemy.position = pull(sourcePos, enemy.position, strObjects)

    tempList = enemies["triangles"]
    for enemy in tempList:
        enemy.position = pull(sourcePos, enemy.position, strObjects)

    tempList = enemies["pentagons"]
    for enemy in tempList:
        enemy.position = pull(sourcePos, enemy.position, strObjects)

    tempList = enemies["hexegons"]
    for enemy in tempList:
        enemy.position = pull(sourcePos, enemy.position, strObjects)


# Pull function for gravity pull
def pull(posSource, posPulled, force):
    dX = posSource[0] - posPulled[0]
    dY = posSource[1] - posPulled[1]
    dH = sqrt(dX * dX + dY * dY)

    return [posPulled[0] + (force * dX / dH), posPulled[1] + (force * dY / dH)]


# Moves the player ship
def moveMyShip():
    global MyShip
    enemies = create.enemies

    shipObj = MyShip["object"]
    # Left - Right Rotate
    if MyShip["left"] == True: shipObj.rotation -= MyShip["rotationSpeed"]
    if MyShip["right"] == True: shipObj.rotation += MyShip["rotationSpeed"]
    shipObj.direction = shipObj.rotation
    # Up - Go forward, stop
    if MyShip["up"] == True:
        shipObj.speed = MyShip["speed"]
    else:
        shipObj.speed = 0
    # Down - Half Speed
    if MyShip["down"] == True: shipObj.speed = shipObj.speed / 2

    # Shooting speed upgrade
    if MyShip["score"] >= 2000:
        MyShip["timerUpgrade"] = 3
    elif MyShip["score"] >= 1000:
        MyShip["timerUpgrade"] = 2
    elif MyShip["score"] >= 500:
        MyShip["timerUpgrade"] = 1

    # Spacebar - Fire
    MyShip["timer"] -= 1
    if MyShip["timer"] < 0: MyShip["timer"] = 0
    if MyShip["spacebar"] == True:
        if MyShip["timer"] == 0:
            fire()
            MyShip["timer"] = MyShip["timerMax"] - MyShip["timerUpgrade"]

    # Explode
    if MyShip["score"] - MyShip["explode"] >= 1000:
        MyShip["explode"] += 1000
        numBullets = int(15 + 15 * MyShip["timerUpgrade"])
        for i in xrange(numBullets):
            newBullet = generators["bulletGen"].next()
            newBullet.position = list(MyShip["object"].position)
            newBullet.direction = i * 2 * pi / numBullets
            MyShip["bullets"].append(newBullet)


# Checks all collisions
def checkCollisions():
    global MyShip
    enemies = create.enemies
    polygonShapes = create.polygonShapes

    shipObj = MyShip["object"]
    bullets = MyShip["bullets"]

    # Check triangles
    tempList = enemies["triangles"]
    for enemy in tempList:
        if shipObj.collidesObject(enemy):
            lose()
            return
        for bullet in bullets:
            if enemy.collidesBullet(bullet):
                MyShip["bullets"].remove(bullet)
                enemy.health -= 1
                if enemy.health == 0:
                    MyShip["score"] += 20
                    enemies["triangles"].remove(enemy)
                    break

    # Check squares
    tempList = enemies["squares"]
    for enemy in tempList:
        if shipObj.collidesObject(enemy):
            lose()
            return
        for bullet in bullets:
            if enemy.collidesBullet(bullet):
                MyShip["bullets"].remove(bullet)
                enemy.health -= 1
                if enemy.health == 0:
                    MyShip["score"] += 35
                    createTriangle(enemy.position)
                    createTriangle(enemy.position)
                    enemies["squares"].remove(enemy)
                    break

    # Check pentagons
    tempList = enemies["pentagons"]
    for enemy in tempList:
        if shipObj.collidesObject(enemy):
            lose()
            return
        for bullet in bullets:
            if enemy.collidesBullet(bullet):
                MyShip["bullets"].remove(bullet)
                enemy.health -= 1
                if enemy.health == 0:
                    MyShip["score"] += 100
                    enemies["pentagons"].remove(enemy)
                    break
                else:
                    enemy.shape = polygonShapes[enemy.health - 1]
                    MyShip["score"] += 10
                    createPenTri(enemy.position)

    # Check hexegons
    tempList = enemies["hexegons"]
    for enemy in tempList:
        if shipObj.collidesObject(enemy):
            lose()
            return
        for square in enemies["squares"]:
            if enemy.collidesObject(square):
                enemy.health += 1
                createTriangle(square.position)
                createTriangle(square.position)
                createTriangle(square.position)
                enemies["squares"].remove(square)

        for pentagon in enemies["pentagons"]:
            if enemy.collidesObject(pentagon):
                enemy.health += 1
                createPenTri(pentagon.position)
                createPenTri(pentagon.position)
                createPenTri(pentagon.position)
                enemies["pentagons"].remove(pentagon)

        for bullet in bullets:
            if enemy.collidesBullet(bullet):
                MyShip["bullets"].remove(bullet)
                enemy.health -= 1
                if enemy.health == 0:
                    MyShip["score"] += 150
                    enemies["hexegons"].remove(enemy)
                    break

    # Hexegons gain health by destroying big objects. This will create 1 more traingle

    # Check myGod
    tempList = enemies["myGod"]
    for enemy in tempList:
        if shipObj.collidesObject(enemy):
            lose()
            return
        for bullet in bullets:
            if enemy.collidesBullet(bullet):
                MyShip["bullets"].remove(bullet)
                enemy.health -= 1
                if enemy.health <= 18:
                    enemy.speed = 0
                if enemy.health == 0:
                    MyShip["score"] += 400
                    enemies["myGod"].remove(enemy)
                    break


# You lose the game
def lose():
    global MyShip
    if MyShip["godMode"] == 0: MyShip["dead"] = True


'''Helper Functions'''


# This fires a bullet
def fire():
    global MyShip
    global generators

    newBullet = generators["bulletGen"].next()
    newBullet.position = list(MyShip["object"].position)
    newBullet.direction = MyShip["object"].direction
    MyShip["bullets"].append(newBullet)


# This is the code that creates all enemies
def createRandom():
    global MyShip
    enemies = create.enemies

    probability = random.randint(0, 400)
    score = MyShip["score"]

    # Create squares
    if len(enemies["squares"]) < 6 + score / 350:
        chance = 3 + score / 400
        if probability < chance:
            createRandomSquare()

    # Create pentagons
    if score <= 200: return
    if len(enemies["pentagons"]) < 3 + score / 600:
        chance = 1.2 + score / 8000
        if probability < chance:
            createRandomPentagon()

    # Create hexagons
    if score <= 800: return
    if len(enemies["hexegons"]) < 1 + score / 1000:
        chance = 0.4 + score / 1500
        if probability < chance:
            createRandomHexegon()

    # Create myGod
    if score <= 2000: return
    if len(enemies["myGod"]) < 0.5 + score / 2000:
        chance = score / 2500
        if probability < chance:
            createRandomMyGod()
