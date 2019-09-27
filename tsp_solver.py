# coding: utf-8
import sys
import random
from cityClass import City
### given list of int with city indices, create csv file
### input: list of int
### output: .csv with single column city indices
def createCSV(arg):
    len = len(arg)
    csv = open('solution.csv', 'w')
    for i in range(len):
        data = arg[i]
        csv.write(data)
    return csv

### get initial population using random shuffle. Number of initial population able to assign.
### input: number of cities, num of initial population
### output: list of list of int(city)
def initialPopulation(num, pop):
    population = []
    alignedList = list(range(1, num+1))
    for i in list(range(1, pop+1)):
        random.shuffle(alignedList)
        population.append(alignedList)
    return population
#print(initialPopulation(5, 3))

'''
def initialPopulationMST(num, pop):
    population = []
    alignedList = list(range(1, num+1))
'''
'''
### calculate fitness: total distance between cities
### input: list of int
### output: int
def getFitness(li):
    for i in li:
        a = City(i, xxx, yyy)
'''

'''
def select()
def getFitness()
def crossover()
def mutate()
'''

### main function
### input: -
### output: .csv
def main():
    prob = sys.argv[1]
    prob_open = open(prob, 'r')
    #pop = sys.argv[2]
    lines = prob_open.readlines()
    len = lines[3]
    num = int(len[12:])
    lines = lines[6:]
    lines = [i.split(" ") for i in lines]
    cities = []
    for i in range(0, num):
        x = lines[i][1]
        y = lines[i][2]
        cities.append(City(i, x, y))
    
    #print(lines[:12])


    #initialPopulation = initialPopulation(num, pop)

    

    prob_open.close()    

main()