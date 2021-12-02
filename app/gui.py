# Copyright (c) 2011 Cosku Acay, http://www.coskuacay.com

import create
import smart
from main import *
from Tkinter import *
#THIS HANDLES GUI EVENTS

options = {"background":"white", "win_width":800, "win_ratio":0,
           "myRotation":radians(10), "mySpeed":15}

#Globals
gameStarted = 0

#Starts new game
def start():
    global gameStarted
    MyShip=create.MyShip

    #Initialize enemy dictionary
    create.enemies = {"squares":[], "triangles":[], "pentagons":[], "hexegons":[], "myGod":[]}

    #MyShip
    height = options["win_width"] / options["win_ratio"]
    MyShip["object"].position = [options["win_width"]/2, height/2]
    MyShip["object"].rotation= -pi/2
    
    MyShip["score"] = 0
    MyShip["timerMax"]=4     #For interval between bullets
    MyShip["timer"]=0        #Current wait time
    MyShip["timerUpgrade"]=0 #Upgrade shooting speed with score
    MyShip["bullets"] = []   #Store bullet object here

    MyShip["explode"] = 0    #Last time explosion occured
    MyShip["godMode"] = 0    #Enables god mode

    #These are for moving around
    MyShip["spacebar"]=False
    MyShip["paused"]=False
    MyShip["dead"]=False
    MyShip["up"]=False
    MyShip["down"]=False
    MyShip["left"]=False
    MyShip["right"]=False
    MyShip["speed"]=options["mySpeed"]
    MyShip["rotationSpeed"]=options["myRotation"]

    #Create four initial squares
    for index in xrange(4):
        createRandomSquare()
    redraw()
    if gameStarted==0:
        gameStarted=1
        timerFired()

#Draw everything on canvas
def redraw():
    global canvas
    global options
    MyShip = create.MyShip
    display = smart.display  #For scale factor
    enemies = create.enemies

    canvas.delete(ALL)
    #Draw the background
    canvas.create_rectangle(0,0, canvas.winfo_width(), canvas.winfo_height(),
                            fill=options["background"], outline=options["background"])
    

    #Draw bullets
    tempList = MyShip["bullets"]
    for bullet in tempList:
        bullet.draw()

    #Draw enemies
    tempList = enemies["triangles"]
    for enemy in tempList:
        enemy.draw()

    #Draw player ship
    MyShip["object"].draw()

    #Draw myGod Particles
    tempList = enemies["myGod"]
    for enemy in tempList:
        enemy.draw()

    #Draw enemies
    tempList = enemies["squares"]
    for enemy in tempList:
        enemy.draw()

    tempList = enemies["pentagons"]
    for enemy in tempList:
        enemy.draw()

    tempList = enemies["hexegons"]
    for enemy in tempList:
        enemy.draw()

    s = display[2] #The scale factor for displaying text
    #Draw score
    x = canvas.winfo_width()
    y = canvas.winfo_height()
    canvas.create_text(x-225*s, y-10*s, text= "Score: " + str(MyShip["score"]),
                       fill="black", font=("Helvetica", int(25*s), "bold"), anchor=SW)

    #Draw Paused message if so
    if MyShip["dead"]==True:
        canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2-60*s,
                           text="GAME OVER", fill="red", font=("Helvetica", int(80*s), "bold"))
        canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2+10*s,
                           text="Press <spacebar> to restart...", fill="black",
                           font=("Helvetica", int(20*s), "bold"))

    #Draw Dead message if so
    if MyShip["paused"]==True:
        canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2-60*s,
                           text="PAUSED", fill="red", font=("Helvetica", int(80*s), "bold"))
        canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2+10*s,
                           text="Press <P> to continue...", fill="black",
                           font=("Helvetica", int(20*s), "bold"))

#The timer
def timerFired():
    global canvas
    MyShip = create.MyShip

    changeSize=resize()
    if MyShip["paused"]==False and MyShip["dead"]==False:
        checkCollisions()
        if MyShip["dead"]==False:
            moveMyShip()
            createRandom()
            stepAll()
        redraw()
    elif changeSize==True: redraw()
    canvas.after(1000/60, timerFired)

#Get Keys to move MyShip
def keyDown(event):
    MyShip = create.MyShip
    key = event.keysym.lower()
    
    if key == "p": #Pause
        if MyShip["paused"] ==False:
            if MyShip["dead"]==False:
                MyShip["paused"]=True
                redraw()
        else:
            MyShip["paused"]=False

    elif key == "space": #Spacebar
        if MyShip["dead"] ==False:
            MyShip["spacebar"]=True
        else:
            start()
    elif key == "up": #Up key
        MyShip["up"]=True
    elif key == "down": #Down key
        MyShip["down"]=True
    elif key == "right": #Right key
        MyShip["right"]=True
    elif key == "left": #Left key
        MyShip["left"]=True

def keyUp(event):
    MyShip = create.MyShip
    key = event.keysym.lower()

    if key == "space": #Spacebar
        MyShip["spacebar"]=False
    elif key == "up": #Up key
        MyShip["up"]=False
    elif key == "down": #Down key
        MyShip["down"]=False
    elif key == "right": #Right key
        MyShip["right"]=False
    elif key == "left": #Left key
        MyShip["left"]=False

    #Test Code
    elif key == "return":
        createRandomMyGod()
    elif key == "g":
        MyShip["godMode"] = (1-MyShip["godMode"])

#This handles window resizing
def resize():
    global canvas
    global options
    global frame
    global lastSize

    widthNew = frame.winfo_width()
    heightNew = frame.winfo_height()
    if widthNew==lastSize[0] or heightNew==lastSize[1]: return False
    
    display = smart.display  #For scale factor
    
    if float(widthNew) / heightNew > options["win_ratio"]:
        canvas.config(width=heightNew*options["win_ratio"], height=heightNew)
        canvas.pack(side=TOP)
    else:
        canvas.config(width=widthNew, height=widthNew/options["win_ratio"])
        canvas.pack(side=LEFT)

    display[2]=float(canvas.winfo_width())/options["win_width"] #Scale factor
    return True


#Create GUI and initialize everything
def run():
    global canvas    #The Canvas
    global options   #Game options
    global lastSize  #To resize the window
    global frame     #To resize the window

    #Create the window
    root = Tk()
    root.bind("<Any-KeyPress>",keyDown)
    root.bind("<Any-KeyRelease>",keyUp)

    #Set the window size
    try:
        #On MS Windows set "zoomed" state.
        root.wm_state('zoomed')
    except:
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight() - 60
        root.wm_geometry("%dx%d+0+0" % (w,h))
    
    #Create a frame to hold the canvas
    frame = Frame(root, bg="black", takefocus=False)
    frame.pack(fill=BOTH, expand=1)

    #Create the canvas
    canvas=Canvas(frame, takefocus=False)
    canvas.pack()

    #Other Window Stuff
    root.title("Polygon Game ~ Cosku Acay")
    root.update()

    #Set display options
    if options["win_ratio"]==0:
        options["win_ratio"] = float(frame.winfo_width()) / frame.winfo_height()
    smart.display = [options["win_width"],options["win_width"]/options["win_ratio"],1]
    lastSize = [0,0]
    
    #Initialize and start timer
    init(canvas)
    start()

    root.mainloop()
