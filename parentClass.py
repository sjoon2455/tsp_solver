#coding: utf-8

class Parent:
    def __init__(self, li, fit):
        self.li = li
        self.fit = fit
    
    def getFitness(self):
        return self.fit