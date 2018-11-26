from soccerBall import soccerBall
import math

class playerVisiting(object):
    #Model
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = 0.1
        self.r = 15
        self.jersey = "Red"
    #View
    def draw(self,canvas):
        canvas.create_oval(self.x - self.r,self.y - self.r,self.x + self.r
        ,self.y + self.r,fill = self.jersey)
    
    #Control
    def move(self,direction,speed):
        self.x = self.x + self.speed * math.cos(math.radians(direction))
        self.y = self.y - self.speed * math.sin(math.radians(direction))
        
    # Check if the visiting player collides with the ball or not
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
    
    #Return the direction of where the ball should move
    def ballChasingDirection(self,other):
        if(not isinstance(other,soccerBall)):
            return False
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
            return finalDirection
                
        