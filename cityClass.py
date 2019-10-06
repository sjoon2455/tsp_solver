# coding: utf-8
# n, x, y: int
class City:
    def __init__(self, n, x, y):
        self.n = n
        self.x = x
        self.y = y
    
    def getDistance(self, c):
        return(   ((self.getX()-c.getX())**2+(self.getY()-c.getY())**2)**0.5 )
    def getIndex(self):
        return self.n
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y