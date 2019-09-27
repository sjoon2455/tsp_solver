#coding: utf-8

### li: list of City(), fit: fitness value
class Parent:
    def __init__(self, li, fit):
        self.li = li
        self.fit = fit
    
    def getFitness(self):
        return self.fit
    
    def setProbability(self, prob):
        self.prob = prob
        return 1
    
    def getList(self):
        return self.li