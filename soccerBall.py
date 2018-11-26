import math

class soccerBall(object):
    #Model
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.r = 10
    #View
    def draw(self,canvas):
        canvas.create_oval(self.x - self.r,self.y - self.r,self.x + self.r
        ,self.y + self.r,fill = "Black")
        
    def bouncingBoarder(self,direction,leftBoarder,rightBoarder,lowerBoarder,upperBoarder,bouncedDirection):
        if((self.x - self.r < leftBoarder) and direction <= 180 and direction >= 90):
            direction = direction - 2 * (direction - 90)
            return [True,direction]
        if((self.x - self.r < leftBoarder) and direction >= 180 and direction <= 270):
            direction = direction + 2 * (270 - direction)
            return [True,direction]
        if((self.x + self.r > rightBoarder) and direction >= 0 and direction <= 90):
            direction = direction + 2 * (90 - direction)
            return [True,direction]
        if((self.x + self.r > rightBoarder) and direction >= 270 and direction <= 360):
            direction = direction - 2 * (direction - 270)
            return [True,direction]
        if((self.y - self.r < lowerBoarder) and direction >= 0 and direction <= 90):
            direction = 360 - direction
            return [True,direction]
        if((self.y - self.r < lowerBoarder) and (self.x < 187.5 or self.x > 312.5) and direction >= 90 and direction <= 180):
            direction = direction + 2 * (180 - direction)
            return [True,direction]
        if((self.y + self.r > upperBoarder) and (self.x < 187.5 or self.x > 312.5) and direction >= 270 and direction <= 360):
            direction = 360 - direction
            return [True,direction]
        if((self.y + self.r > upperBoarder) and (self.x < 187.5 or self.x > 312.5) and direction >= 180 and direction <= 270):
            direction = direction - 2 * (direction - 180)
            return [True,direction]
        else:
            return [False,bouncedDirection]
            
    #Control
    def reactToKick(self,direction,speed):
        self.x = self.x + speed * math.cos(math.radians(direction))
        self.y = self.y - speed * math.sin(math.radians(direction))
    
    def collideWithVisitingTeamCheck(self,other):
        from playerVisiting import playerVisiting
        if(not isinstance(other,playerVisiting)):
            return False
        else:
            dist = ((other.x-self.x)**2 + (other.y - self.y)**2)**0.5
            if(dist < self.r + other.r):
                return True
                
    def collideWithHomeTeamCheck(self,other):
        from playerHome import playerHome
        if(not isinstance(other,playerHome)):
            return False
        else:
            dist = ((other.x-self.x)**2 + (other.y - self.y)**2)**0.5
            if(dist < self.r + other.r + 10):
                return True