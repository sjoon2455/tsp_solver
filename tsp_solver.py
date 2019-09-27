# coding: utf-8
import sys
import random
from cityClass import City
from parentClass import Parent

################################################# MAJOR FUNCTION #################################################
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


### calculate fitness: total distance between cities
### input: list of int
### output: int
def computeFitness(route, cities):
    distance = 0
    actualRoute = [cities[i-1] for i in route]
    length = len(actualRoute)
    # starts with i=0
    for i in range(length):
        if i == (length-1):
            distance += actualRoute[i].getDistance(actualRoute[0])
        else:
            distance += actualRoute[i].getDistance(actualRoute[i+1])
    return distance
        





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


################################################# HELPER FUNCTION #################################################
### add all fitness values of current population
### input: list of parents
### output: int
def sumFitness(parents):
    res = 0
    for i in parents:
        fit = i.getFitness()
        res += fit
    return res


################################################# MAIN FUNCTION #################################################
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
        x = int(lines[i][1])
        y = int(lines[i][2])
        cities.append(City(i+1, x, y))
    initialPopulation = initialPopulation(num, pop)
    
    # main loop
    count = 0
    while count < loop:
        count += 1
        parents = []
        #route: [3, 5, 61, 24, 6, ..., 2412]
        for route in initialPopulation:
            fitness = computeFitness(route, cities)
            parent = Parent(route, fitness)
            parents.append()
        sumFitness = sumFitness(parents)
    


    

    

    prob_open.close()    

main()