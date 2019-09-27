# coding: utf-8
import sys
import random
from cityClass import City
from parentClass import Parent
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

### calculate fitness: total distance between cities
### input: list of int
### output: int
def getFitness(route, cities):
    distance = 0
    actualRoute = [cities[i-1] for i in route]
        


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
    pop = sys.argv[2]
    loop = sys.argv[3]

    lines = prob_open.readlines()
    len = lines[3]
    num = int(len[12:])
    lines = lines[6:]
    lines = [i.split(" ") for i in lines]
    #cities: list of City()
    cities = []
    for i in range(0, num):
        x = lines[i][1]
        y = lines[i][2]
        cities.append(City(i, x, y))
    initialPopulation = initialPopulation(num, pop)
    
    count = 0
    while count < loop:
        count += 1
        parents = []
        #route: [3, 5, 61, 24, 6, ..., 2412]
        for route in initialPopulation:
            fitness = getFitness(route, cities)
            parent = Parent(route, fitness)
            parents.append()
    
    
    #print(lines[:12])


    

    

    prob_open.close()    

main()