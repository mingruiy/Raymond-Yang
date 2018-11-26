from playerVisiting import playerVisiting
from soccerBall import soccerBall
import math
class playerHome(object):
    #Model
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.initialX = self.x
        self.initialY = self.y
        self.speed = 10
        self.r = 15
        self.jersey = "Blue"
    #View
    def draw(self,canvas):
        canvas.create_oval(self.x - self.r,self.y - self.r,self.x + self.r
        ,self.y + self.r,fill = self.jersey)
    
    #Control
    def reset(self):
        self.x = self.initialX
        self.y = self.initialY
    def move(self,direction):
        if(direction == "up"):
            self.x = self.x + self.speed * math.cos(math.radians(90))
            self.y = self.y - self.speed * math.sin(math.radians(90))
        elif(direction == "down"):
            self.x = self.x + self.speed * math.cos(math.radians(270))
            self.y = self.y - self.speed * math.sin(math.radians(270))
        elif(direction == "left"):
            self.x = self.x + self.speed * math.cos(math.radians(180))
            self.y = self.y - self.speed * math.sin(math.radians(180))
        elif(direction == "right"):
            self.x = self.x + self.speed * math.cos(math.radians(0))
            self.y = self.y - self.speed * math.sin(math.radians(0))
    def collideWithWallCheck(self,leftBoarder,rightBoarder,lowerBoarder,upperBoarder):
        if(self.x-self.r < 80):
            self.x = 90
        if(self.x + self.r > 420):
            self.x = 410
        if(self.y-self.r < 30):
            self.y = 40
        if(self.y + self.r > 470):
            self.y = 460
    def collideWithOtherTeamCheck(self,other):
        if(not isinstance(other,playerVisiting)):
            return False
        else:
            dist = ((other.x-self.x)**2 + (other.y-self.y)**2)**0.5
            if(dist < self.r + other.r and other.x-self.x >= 0 and other.y-self.y<0):
                return "down",True
            if(dist < self.r + other.r and other.x-self.x < 0 and other.y-self.y<0):
                return "down",True
            if(dist < self.r + other.r and other.x-self.x < 0 and other.y-self.y>0):
                return "up",True
            if(dist < self.r + other.r and other.x-self.x >= 0 and other.y-self.y>0):
                return "up",True
            if(dist < self.r + other.r and other.x-self.x > 0 and other.y-self.y==0):
                return "left",True
            if(dist < self.r + other.r and other.x-self.x < 0 and other.y-self.y==0):
                return "right",True
    
    def collideWithSameTeamCheck(self,other):
        if(not isinstance(other,playerHome)):
            return False
        else:
            dist = ((other.x-self.x)**2 + (other.y-self.y)**2)**0.5
            if(dist < self.r + other.r and other.x-self.x >= 0 and other.y-self.y<0):
                return "down",True
            if(dist < self.r + other.r and other.x-self.x < 0 and other.y-self.y<0):
                return "down",True
            if(dist < self.r + other.r and other.x-self.x < 0 and other.y-self.y>0):
                return "up",True
            if(dist < self.r + other.r and other.x-self.x >= 0 and other.y-self.y>0):
                return "up",True
            if(dist < self.r + other.r and other.x-self.x > 0 and other.y-self.y==0):
                return "left",True
            if(dist < self.r + other.r and other.x-self.x < 0 and other.y-self.y==0):
                return "right",True
                
    def collideWithSoccerBallCheck(self,other):
        if(not isinstance(other,soccerBall)):
            return False
        else:
            dist = ((other.x-self.x)**2 + (other.y-self.y)**2)**0.5
            if((other.x-self.x) == 0 and other.y < self.y):
                theta = 90
                finalDirection = 90
            elif((other.x-self.x) == 0 and other.y > self.y):
                theta = 270
                finalDirection = 270
            elif((other.x-self.x) > 0 and other.y == self.y):
                theta = 0
                finalDirection = 0
            elif((other.x-self.x) < 0 and other.y == self.y):
                theta = 0
                finalDirection = 180
            else:
                theta = math.atan((abs(other.y - self.y))/(abs(other.x-self.x)))
                theta = math.degrees(theta)
                if(other.x-self.x)>0 and (other.y-self.y)<0:
                    finalDirection = theta
                if(other.x-self.x<0) and (other.y-self.y)<0:
                    finalDirection = 180-theta
                if(other.x-self.x<0) and (other.y-self.y)>0:
                    finalDirection = 180+theta
                if(other.x-self.x>0) and (other.y-self.y)>0:
                    finalDirection = 360-theta
            return dist < self.r + other.r,finalDirection
            
    def thePlayerOnHold(self,other):
        if(not isinstance(other,soccerBall)):
            return False
        else:
            dist = ((other.x - self.x)**2 + (other.y - self.y)**2)**0.5
            if(dist < (self.r + other.r + 5)):
                return True
        
