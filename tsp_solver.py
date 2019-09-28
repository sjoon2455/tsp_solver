# coding: utf-8
import sys
import random
import datetime
from cityClass import City
from parentClass import Parent
from geneIndexClass import Geneindex
from printPretty import printPretty
import math


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

### get cumulative probability of given Parent()s as a list
### input: list of Parent()
### output: list of float
def getCumulProb(parents):
    res = []
    i = 0
    for parent in parents:
        prob = parent.getProbability()
        if i == 0:
            res[i] = prob
        else:
            res[i] = res[i-1] + prob
        i += 1
    return res

### Check if picked with a probability of r
### input: num(not used), probability(0~1.0)
### output: boolean
def isPicked(num, r):
    sampleSpace = []
    firstdecimal_r = math.round(r*10)/10
    win = int(firstdecimal_r * 10)
    lose = 10 - win
    for i in range(win):
        sampleSpace.append(1)
    for j in range(lose):
        sampleSpace.append(0)
    lottery = random.choice(sampleSpace)
    return True if lottery == 1 else False
    


### breed a child b/w dad Parent() and mom Parent() with crossover rate r
### input: Parent(), Parent(), float(0~1)
### output: Parent()
def breed(dad, mom, r):
    crossover_cities = []
    dadRoute = dad.getList()
    momRoute = mom.getList()
    index = 0
    #type check necessary
    for i in dadRoute:
        if isPicked(i, r):
            a = Geneindex(i, index)
            crossover_cities.append(a)
            momRoute.replace(i, 0)
        index += 1
    for j in crossover_cities:
        momRoute[j.getIndex()] = j.getNum()
    child = Parent(momRoute, 0)
    return child

### randomly create pairs of Parent()s
### input: list of Parent()
### output: list of pair of Parent()
def makePair(parents)
    pairs = []
    length = len(parents)
    if length % 2 == 0:
        while(len(parents) != 0):
            dad = random.choice(parents)
            parents.remove(dad)
            mom = random.choice(parents)
            parents.remove(mom)
            pairs.append(list(dad, mom))
    else:
        while(len(parents) != 1):
            dad = random.choice(parents)
            parents.remove(dad)
            mom = random.choice(parents)
            parents.remove(mom)
            pairs.append(list(dad, mom))
        pairs.append(list(parents[0]))
    return pairs


        
### swap two num within a list under some probability
### input: list of int, probability r(0~1.0)
### output: list of int
def mutateIndividual(li, r):
    for n1 in range(len(li)):
        if random.random() < r:
            n2 = int(random.random() * len(li))
            swap1 = li[n1]
            swap2 = li[n2]
            li[n1] = swap2
            li[n2] = swap1
    return li


################################################# MAJOR FUNCTION #################################################
### get initial population using random shuffle. Number of initial population able to assign.
### input: number of cities, num of initial population
### output: list of list of int(city)
def initialPopulation(num, pop):
    printPretty("Generating intial population...")
    population = []
    alignedList = list(range(1, num+1))
    for i in list(range(1, pop+1)):
        random.shuffle(alignedList)
        population.append(alignedList)
    printPretty("Generated intial population")
    return population


### calculate fitness: total distance between cities
### input: list of int
### output: int
def computeFitness(route, cities):
    printPretty("Computing Fitness...")
    distance = 0
    actualRoute = [cities[i-1] for i in route]
    length = len(actualRoute)
    # starts with i=0
    for i in range(length):
        if i == (length-1):
            distance += actualRoute[i].getDistance(actualRoute[0])
        else:
            distance += actualRoute[i].getDistance(actualRoute[i+1])
    printPretty("Computed FPS")
    return distance
        

### compute each probabilty of being selected proportional to each fitness value
### input: list of Parent(), total sum of fitness
### output: list of Parent()
def computeFPS(parents, sumFitness):
    printPretty("Computing FPS...")
    for parent in parents:
        prob = parent.getFitness() / sumFitness
        parent.setProbability(prob)
    printPretty("Computed FPS")
    return parents


### 룰렛 팔 N개로 N개를 뽑음
### input: list of Parent(), number of next generation
### ouput: list of Parent()
def sampleSUS(parents, N):
    printPretty("Sampling using SUS...")
    selected = [0 for x in range(N)]
    cumul_prob = getCumulProb(parents)
    current_member = 0
    i = 0
    r = random.uniform(0, 1/N)
    while(current_member <= N-1):
        while(r <= cumul_prob[i]):
            selected[current_member] = parents[i]
            r += 1/N
            current_member += 1
        i += 1
    return selected

### Make pairs of Parent()s, randomly and uniformly pick some part and switch the same number sequence retaining its orders
### input: list of Parent(), crossover rate(0~1.0)
### output: list of Parent()
def orderedCrossover(selected, r)
    childs = []
    pairs = makePair(selected)
    for pair in pairs:
        if len(pair) % 2 == 1:
            child = pair[0]
            childs.append(child)
        else:
            child = breed(pair[0], pair[1], r)
            child.append(child)
    return childs

    

### with some probability r, swap two cities
### input: list of Parent(), probability r(0~1.0)
### output: list of Parent()
def mutate(crossovered, r):
    for parent in crossovered:
        li = parent.getList()
        mutated_li = mutateIndividual(li, r)
        parent.setList(mutated_li)


### maintain M best from Parents, get rid of M worst from Current
### input: list of Parent()
### output: list of Parent()
def chooseBestGeneration(mutated)




### choose the best fitness Parent() among Parent()s
### input: list of Parent()
### output: Parent()
def chooseBestOne(pop):
    res = pop[0]
    for parent in pop:
        if parent.getFitness() > res.getFitness():
            res = parent
    return res


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



if __name__ == "__main__"
    main()