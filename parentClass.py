#coding: utf-8

### li: list of City(), fit: fitness value
class Parent:
    prob = 0
    def __init__(self, li, fit):
        self.li = li
        self.fit = fit
    
    def getFitness(self):
        return self.fit
    
    def setProbability(self, prob):
        self.prob = prob
        return 1
    
    def getProbability(self):
        return self.prob
    
    def getList(self):
        return self.li
    
    def setList(self, newli):
        self.li = newli
        return 1