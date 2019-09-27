# coding: utf-8
import sys
import random
import datetime
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
    csv = open('solution_{0}.csv'.format(str(datetime.datetime.now().time())[:-7]), 'w')
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

### list of parent -> list of city indices
### input: list of parent
### output: list of int
def parentToInt(solution)
    res = []
    for parent in solution:
        index = parent.getList().getIndex()
        res.append(index)
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
    population = initialPopulation
    while count < loop:
        count += 1
        selected = []
        parents = []
        #route: [3, 5, 61, 24, 6, ..., 2412]
        for route in population:
            fitness = computeFitness(route, cities)
            parent = Parent(route, fitness)
            parents.append()
        sumFitness = sumFitness(parents)
        parents = computeFPS(parents, sumFitness)
        selected = sampleSUS(parents, pop)
        crossovered = orderedCrossover(selected)
        mutated = mutate(crossovered)
        population = chooseBestGeneration(mutated)
    theBestOne = chooseBestOne(population)
    solution = parentToInt(theBestOne)
    createCSV(solution)

    prob_open.close()    



### compute each probabilty of being selected proportional to each fitness value
### input: list of list of Parent(), total sum of fitness
### output: list of list of Parent()
def computeFPS(parents, sumFitness)

### 룰렛 팔 N개로 N개를 뽑음
### input: list of list of Parent(), number of next generation
### ouput: list of list of Parent()
def sampleSUS(parents, N)

### Make pairs of Parent()s, randomly and uniformly pick some part and switch the same number sequence retaining its orders
### input: list of list of Parent(), crossover rate(0~1.0)
### output: list of list of Parent()
def orderedCrossover(selected, r)

### 
def mutate(crossovered, r)

### maintain M best from Parents, get rid of M worst from Current
### input: list of list of Parent()
### output: list of list of Parent()
def chooseBestGeneration(mutated)

main()