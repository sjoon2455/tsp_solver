class City:
    def __init__(self, n, x, y):
        self.n = n
        self.x = x
        self.y = y
    
    def distance(self, c):
        return(((self.x-c.x)**2+(self.y-c.y)**2)**0.5)