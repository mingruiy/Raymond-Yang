from tkinter import *
from playerHome import playerHome
from playerVisiting import playerVisiting
from soccerBall import soccerBall
import math
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.playerHomeIndex = 0
    data.playerVisitingIndex = 0
    data.picture = PhotoImage(file = "newSoccer pitch.png")
    data.picture = data.picture.subsample(2,2)
    data.leftPostX = 187.5
    data.rightPostX = 312.5
    data.leftBoarder = 80
    data.rightBoarder = 420
    data.lowerBoarder = 30
    data.upperBoarder = 470
    data.soccerBall = soccerBall(data.width/2,data.height/2) 
    data.soccerMovingState = False
    #data.collided means when the soccer ball collides with the visiting player
    data.collided = False
    data.bouncedWall = False
    data.direction = 0
    data.bouncedDirection = 0
    data.collidedSpeed = 0
    data.ballSpeed = 1.5
    data.blueTeamScore = 0
    data.redTeamScore = 0
    data.startingPostionHome = [[200,300],[300,300],[250,450]]
    data.team1 = [playerHome(data.startingPostionHome[0][0],data.startingPostionHome[0][1]),playerHome(data.startingPostionHome[1][0],data.startingPostionHome[1][1]),playerHome(data.startingPostionHome[2][0],data.startingPostionHome[2][1])]
    data.team2 = [playerVisiting(200,200),playerVisiting(250,50),playerVisiting(300,200)]

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if(event.keysym == "Up"):
        data.team1[data.playerHomeIndex].move("up")
        data.team1[data.playerHomeIndex].speed = 10
    if(event.keysym == "Down"):
        data.team1[data.playerHomeIndex].move("down")
        data.team1[data.playerHomeIndex].speed = 10
    if(event.keysym == "Left"):
        data.team1[data.playerHomeIndex].move("left")
        data.team1[data.playerHomeIndex].speed = 10
    if(event.keysym == "Right"):
        data.team1[data.playerHomeIndex].move("right")
        data.team1[data.playerHomeIndex].speed = 10
    pass

def visitingTeamRespond(data):
    newDirection = data.team2[data.playerVisitingIndex].ballChasingDirection(data.soccerBall)
    data.team2[data.playerVisitingIndex].move(newDirection,data.team2[data.playerVisitingIndex].speed)
    
def timerFired(data):
    #Make one of the visiting team player to chase the ball
    visitingTeamRespond(data)
    
    #Check if the soccer has scored
    if(data.soccerBall.y < 30 and data.soccerBall.x > data.leftPostX and data.soccerBall.x < data.rightPostX):
        data.blueTeamScore = data.blueTeamScore + 1
        data.soccerBall.y = data.width/2
        data.soccerBall.x = data.height/2
        data.ballSpeed= 0
        data.team1[data.playerHomeIndex].reset()
        print(data.blueTeamScore)
        
    #Normal moving state
    if(data.soccerMovingState == True):
        if(data.collided == False and data.bouncedWall == False):
            data.ballSpeed = data.ballSpeed - 0.01
            if(abs(data.ballSpeed-0)<0.02):
                data.soccerMovingState = False
                data.ballSpeed = 1.5
            data.soccerBall.reactToKick(data.direction,data.ballSpeed)
            
    #Check if the player hits a wall. If he hits a wall, makes him freeze
    data.team1[data.playerHomeIndex].collideWithWallCheck(data.leftBoarder,data.rightBoarder,data.lowerBoarder,data.upperBoarder)
    
    #Check if a player hits a visiting team player, if so, he can't move forward anymore. 
    for i in data.team2:
        if(data.team1[data.playerHomeIndex].collideWithOtherTeamCheck(i)):
            data.team1[data.playerHomeIndex].move(data.team1[data.playerHomeIndex].collideWithOtherTeamCheck(i)[0])
    #Check if a player hits a home team player, if so, he can't move forward anymore
    for i in range(len(data.team1)):
        if(i == data.playerHomeIndex):
            continue
        else:
            if(data.team1[data.playerHomeIndex].collideWithSameTeamCheck(data.team1[i])):
                data.team1[data.playerHomeIndex].move(data.team1[data.playerHomeIndex].collideWithSameTeamCheck(data.team1[i])[0])
            
    #Check if the player hits a soccer ball
    if(data.team1[data.playerHomeIndex].collideWithSoccerBallCheck(data.soccerBall)[0]):
        data.soccerMovingState = True
    data.direction = data.team1[data.playerHomeIndex].collideWithSoccerBallCheck(data.soccerBall)[1]
    
    #Check if the ball collides with the wall or not
    if(data.soccerBall.bouncingBoarder(data.direction,data.leftBoarder,data.rightBoarder,data.lowerBoarder,data.upperBoarder,data.bouncedDirection)[0] == True):
        data.bouncedWall = True
    if(data.bouncedWall == True) and (data.soccerMovingState == True):
        data.bouncedDirection = data.soccerBall.bouncingBoarder(data.direction,data.leftBoarder,data.rightBoarder,data.lowerBoarder,data.upperBoarder,data.bouncedDirection)[1]
        data.ballSpeed = data.ballSpeed - 0.01
        if(abs(data.ballSpeed - 0) < 0.02):
            data.soccerMovingState = False
            data.ballSpeed = 0
            data.bouncedWall = False
        data.soccerBall.reactToKick(data.bouncedDirection,data.ballSpeed)

    #Check if the ball collide with Visiting player
    for i in data.team2:
        if(data.soccerBall.collideWithVisitingTeamCheck(i) and data.soccerMovingState == True):
            data.collided = True
            data.collidedSpeed = -data.ballSpeed
    if(data.soccerMovingState == True and data.collided == True):
        data.collidedSpeed = data.collidedSpeed + 0.04
        if(abs(data.collidedSpeed-0)<0.02):
            data.soccerMovingState = False
            data.collided = False
        data.soccerBall.reactToKick(data.team1[data.playerHomeIndex].collideWithSoccerBallCheck(data.soccerBall)[1],data.collidedSpeed)
        
    #Check if the ball collide with Home player
    for i in range(len(data.team1)):
        if(i == data.playerHomeIndex):
            continue
        else:
            if(data.soccerBall.collideWithHomeTeamCheck(data.team1[i]) and data.soccerMovingState == True):
                data.collided = True
                data.collidedSpeed = -data.ballSpeed
                data.playerHomeIndex = i
    if(data.soccerMovingState == True and data.collided == True):
        data.collidedSpeed = data.collidedSpeed + 0.1
        print("data.collidedSpeed",data.collidedSpeed)
        if(abs(data.collidedSpeed-0)<0.1):
            print("In restriction")
            data.soccerMovingState = False
            data.collided = False
            data.collidedSpeed = 1.5
        data.soccerBall.reactToKick(data.team1[data.playerHomeIndex].collideWithSoccerBallCheck(data.soccerBall)[1],data.collidedSpeed)
    
    #Check which player should actually hold the ball
    # for i in range(len(data.team1)):
    #     if(i == data.playerHomeIndex):
    #         continue
    #     if(data.team1[i].thePlayerOnHold(data.soccerBall) == True):
    #         data.switched == True
    #         print("Successfully Switched")
    #         data.playerHomeIndex = i
    #         print(data.playerHomeIndex)
            
            
def draw(canvas,data):
    canvas.create_image(data.width/2,data.height/2,image = data.picture)
    canvas.create_text(50,50,text = "BlueTeam:%d"%data.blueTeamScore)
    canvas.create_text(50,60,text = "RedTeam:%d"%data.redTeamScore)
    for i in data.team1:
        i.draw(canvas)
    for i in data.team2:
        i.draw(canvas)
    data.soccerBall.draw(canvas)
    
    
def redrawAll(canvas, data):
    # draw in canvas
    draw(canvas, data)
    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.timerDelay = 1
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(500, 500)