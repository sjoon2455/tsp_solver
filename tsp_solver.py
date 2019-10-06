# coding: utf-8
import sys
import random
import datetime
import time
from cityClass import City
from parentClass import Parent
from geneIndexClass import GeneIndex
from printPretty import printPretty as pp
import matplotlib.pyplot as plt
import numpy as np
import copy


################################################# HELPER FUNCTION #################################################
### add all fitness values of current population
### input: list of Parent()
### output: float
def sumFitness(parents):
    res = 0
    for i in parents:
        print("BEFORE SUMFITNESS: ", i.getList()[:5])
        fit = i.getFitness()
        res += fit
    return res

### get fitness values of all individual chromosomes in increasing order
### input: list of Parent
### output: list of float
def getFitnessOfAll(parents):
    res = []
    for parent in parents:
        res.append(parent.getFitness())
    return sorted(res)


### Parent() -> list of city indices
### input: Parent()
### output: list of int
def parentToInt(solution):
    return solution.getList()

### get cumulative probability of given Parent()s as a list
### input: list of Parent()
### output: list of float
def getCumulProb(parents):
    res = []
    i = 0
    for parent in parents:
        prob = parent.getProbability()
        if i == 0:
            res.append(prob)
    
        else:
            res.append(res[-1]+prob)
    
        i += 1
    
    return res

### Check if picked with a probability of r
### input: num(not used), probability(0~1.0)
### output: boolean
def isPicked(num, r):
    sampleSpace = []
    firstdecimal_r = round(r, 1)
    win = int(firstdecimal_r * 10)
    lose = 10 - win
    for i in range(win):
        sampleSpace.append(1)
    for j in range(lose):
        sampleSpace.append(0)
    lottery = random.choice(sampleSpace)
    return True if lottery == 1 else False

### get index of particular value
### input: list of int, int
### output: int
def getIndexList(li, n):
    index = 0
    for i in li:
        if i == n:
            return index
        index += 1

### breed a child b/w dad Parent() and mom Parent() with crossover rate r
### input: Parent(), Parent(), float(0~1)
### output: Parent()
def breed(dad, mom, r, cities):
    crossover_cities = []
    index_mom_list = []
    dadRoute = dad.getList()
    momRoute = mom.getList()
    #print("dadRoute: ", dadRoute)
    #print("momRoute: ", momRoute)
    index_dad = 0
    index_mom = 0
    #type check necessary
    #i: int
    for i in dadRoute:
        if isPicked(i, r):
            a = GeneIndex(i, index_dad) # 1, 2, 4
            crossover_cities.append(a)
            index_mom = getIndexList(momRoute, i) # 3, 5, 6
            index_mom_list.append(index_mom)
        index_dad += 1
    # sort indices in increasing order
    index_mom_list.sort() 
    for j in range(len(crossover_cities)):
        momRoute[index_mom_list[j]] = crossover_cities[j].getNum()
    child_fitness = computeFitness(momRoute, cities)
    child = Parent(momRoute, child_fitness)
    return child

### randomly create pairs of Parent()s
### input: list of Parent()
### output: list of pair of Parent()
def makePair(parents):
    pairs = []
    length = len(parents)
    parentsCopied = parents.copy()
    
    if length % 2 == 0:
        while(len(parentsCopied) != 0):
            dad = random.choice(parentsCopied)
            parentsCopied.remove(dad)
            mom = random.choice(parentsCopied)
            parentsCopied.remove(mom)
            dadAndMom = list()
            dadAndMom.append(dad)
            dadAndMom.append(mom)
            pairs.append(dadAndMom)
        
    else:
        while(len(parentsCopied) != 1):
            dad = random.choice(parentsCopied)
            parentsCopied.remove(dad)
            mom = random.choice(parentsCopied)
            parentsCopied.remove(mom)
            dadAndMom = list()
            dadAndMom.append(dad)
            dadAndMom.append(mom)
            pairs.append(dadAndMom)
        alone = list()
        alone.append(parentsCopied[0])
        pairs.append(alone)
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




### align given list of Parent() with respect to their fitness value in decreasing order
### input: list of Parent()
### output: list of Parent()
def alignFitness(parents):
    return sorted(parents, key = lambda parent : parent.getFitness(), reverse = True)    


################################################# MAJOR FUNCTION #################################################
### get initial population using random shuffle. Number of initial population able to assign.
### input: number of cities, num of initial population
### output: list of Parent()
def initialPopulation(num, pop, cities):
    pp("Generating intial population...")
    population = [0 for x in range(pop)]
    alignedList = list(range(1, num+1))
    # generate random permutated lists
    count = 0
    while count < pop:
        l = copy.copy(alignedList)
        random.shuffle(l) # not aligned anymore
        route = l
        fitness = computeFitness(route, cities)
        population[count] = Parent(route, fitness)
        #for i in range(count+1):
        #    print("THIS: ", population[i].getList()[:5])
        count += 1
        #print("loop {0}, pop: ".format(count), population)
    for i in population:
        print(i.getList()[:5])
    pp("Generated intial population")
    return population


### calculate fitness: total distance between cities
### input: list of int, list of City()
### output: int
def computeFitness(route, cities):
    #pp("Computing Fitness...")
    distance = 0
    actualRoute = [cities[i-1] for i in route] # list of City()
    length = len(actualRoute)
    # starts with i=0
    for i in range(length):
        if i == (length-1):
            distance += actualRoute[i].getDistance(actualRoute[0])
        else:
            distance += actualRoute[i].getDistance(actualRoute[i+1])
    #pp("Computed FPS")
    return distance
        

### compute each probabilty of being selected proportional to each fitness value
### input: list of Parent(), total sum of fitness, list of float
### output: list of Parent()
def computeFPS(parents, sumFitness, everyFitness):
    print("Fitness of all: ", everyFitness)
    minimum = everyFitness[0]
    num = len(parents)
    print("최소: ", minimum)
    print("분모: ", sumFitness-minimum*num)

    for parent in parents:
        print("BEFORE COMPUTEFPS: ", parent.getList()[:5])
        index = getIndexList(everyFitness, parent.getFitness())        
        prob = float(    (everyFitness[-(index+1)]-minimum) / (sumFitness-minimum*num)    )        
        parent.setProbability(prob)
    return parents




### 룰렛 팔 N개로 N개를 뽑음
### input: list of Parent(), number of next generation
### ouput: list of Parent()
def sampleSUS(parents, N):
    for j in parents:
        print("BEFORE SAMPLESUS: ", j.getList()[:5])
    pp("Sampling using SUS...")
    selected = [0 for x in range(N)] #[0, 0, ..., 0]
    cumul_prob = getCumulProb(parents)
    print("누적도수분포: ", cumul_prob)
    current_member = 0
    i = 0
    r = random.uniform(0, 1/N)
    while(current_member <= N-1):
        while(r <= cumul_prob[i]):
            selected[current_member] = parents[i]
            r += 1/N
            current_member += 1
        i += 1
    for p in selected:
        print("BEFORE AAAAAAA: ", p.getList()[:5])
    pp("Sampled using SUS")
    return selected

### Make pairs of Parent()s, randomly and uniformly pick some part and switch the same number sequence retaining its orders
### input: list of Parent(), crossover rate(0~1.0), total population int
### output: list of Parent()
def orderedCrossover(selected, r, pop, cities):
    pp("Crossovering...")
    for p in selected:
        print("Before crossover: ", p.getList()[:5])
    
    
    
    childs = []
    numChild = 0
    numPop = int(0.5*pop if pop%2==0 else 0.5*pop+1)
    #print(numPop) # 6
    while numChild < numPop:
        #print("SELECTED: ", selected)
        pairs = makePair(selected)
        for pair in pairs:
            numChild += 1
            pp("Creating Child #{0}...".format(numChild))
            if len(pair) == 2:
                child = breed(pair[0], pair[1], r, cities)
            else:
                child = pair[0]
            childs.append(child)
    pp("Crossovered")
    return childs

    

### with some probability r, swap two cities
### input: list of Parent(), probability r(0~1.0)
### output: list of Parent()
def mutate(crossovered, r):
    pp("Mutating...")
    for parent in crossovered:
        li = parent.getList()
        print("before mutation getlist: ", li[:5])
        mutated_li = mutateIndividual(li, r)
        print("after mutation getlist: ", mutated_li[:5])
        parent.setList(mutated_li)
    pp("Mutated")
    return crossovered



### update fitness for each Parent()
### input: list of Parent()
### output: list of Parent()
def updateFitness(parents, cities):
    pp("Updating fitness of the mutated...")
    for parent in parents:
        print("!!!!!!!!!!!!!!!!!!!!!: ", parent.getList()[:6])
        fit = computeFitness(parent.getList(), cities)
        parent.setFitness(fit)
        print("updated fit: ",fit)
    
    pp("Updated fitness of the mutated")
    return parents


### maintain M best from Parents, get rid of M worst from Child
### input: list of Parent(), list of Parent(), percentage of elite(0~1.0)
### output: list of Parent()
def chooseBestGeneration(parent, child, m):
    pp("Choosing the best generation...")
    best = []
    l = len(parent)
    #numElite = int(l*m)
    numElite = 2
    aligned_parent = alignFitness(parent)
    best_parent = aligned_parent[:numElite]
    #print("best parent: ", best_parent)
    aligned_child = alignFitness(child)
    best_child = aligned_child[:-numElite]
    #print("best child: ", best_child)
    best = best_parent + best_child
    #print(best)
    pp("Chose the best generation")
    return best




### choose the best fitness Parent() among Parent()s
### input: list of Parent()
### output: Parent()
def chooseBestOne(pop):
    pp("Choosing the best one...")
    res = pop[0]
    for parent in pop:
        if parent.getFitness() > res.getFitness():
            res = parent
    pp("Chose the best one")
    return res


### draw plot end of every loop
### input: list of int, list of float, int, float
### output: -
def drawPlot(x, y, count, theBestFitness):
    
    x.append(count)
    y.append(theBestFitness)
    plt.plot(count, theBestFitness, "ro-")
    plt.show()
    plt.pause(0.0001)
    
    


### given list of int with city indices, create csv file
### input: list of int
### output: .csv with single column city indices
def createCSV(arg):
    pp("Creating CSV file...")
    length = len(arg)
    csv = open('solution_{0}.csv'.format(str(datetime.datetime.now().time())[:-7]), 'w')
    for i in range(length):
        data = str(arg[i])
        csv.write(data+"\n")
    pp("Created CSV file")
    return csv



################################################# MAIN FUNCTION #################################################
### main function
### input: -
### output: .csv
def main():
    prob = sys.argv[1] # file name
    prob_open = open(prob, 'r')
    pop = int(sys.argv[2]) # number of members in population
    loop = int(sys.argv[3]) # number of loop, stop criterion
    elite = float(sys.argv[4]) # elitism percentage to hold til the next generation
    crossoverRate = float(sys.argv[5]) # percentage of being crossovered
    mutationRate = float(sys.argv[6]) # percentage of being mutated
    
    ### for plotting
    plt.ion()
    fig=plt.figure()
    plt.axis([0,loop,0,100000000])
    plt.ylim(bottom = 80000000)
    plt.yscale('log')
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    xlist=list()
    ylist=list()

    lines = prob_open.readlines()
    len = lines[3]
    num = int(len[12:])
    lines = lines[6:]
    lines = [i.split(" ") for i in lines]
    
    #cities: list of City()
    cities = []
    for i in range(0, num):
        x = int(float(lines[i][1]))
        y = int(float(lines[i][2]))
        cities.append(City(i+1, x, y))
    initialPop = initialPopulation(num, pop, cities)
    for k in initialPop:
        print("IIIIIIIIIIIPOPPOPOPOPO: ", k.getList()[:5])
    # main loop
    count = 0
    population = initialPop # list of Parent()
    for i in population:
        print("POPPOPOPOPO: ", i.getList()[:5])
    while count < loop:
        #print("Population of 2nd: ", population)
        count += 1
        selected = []
        sumfit = sumFitness(population)
        everyFitness = getFitnessOfAll(population)
        #print("FITNESS OF ALL: ", everyFitness)
        population = computeFPS(population, sumfit, everyFitness)
        #print("fps computed: ", population)
        selected_parent = sampleSUS(population, int(0.5*pop))
        #print("sus computed: ", selected_parent)
        crossovered_child = orderedCrossover(selected_parent, crossoverRate, pop, cities)
        #print("crossovered: ", crossovered_child)
        mutated_parent = mutate(selected_parent, mutationRate)
        #print("mutated parent: ", mutated_parent)
        mutated_child = mutate(crossovered_child, mutationRate)
        #print("mutated child: ", mutated_child)
        mutated_parent = updateFitness(mutated_parent, cities)
        #print("updated mutated parent: ", mutated_parent)
        mutated_child = updateFitness(mutated_child, cities)
        #print("updated mutated child: ", mutated_child)
        population = chooseBestGeneration(mutated_parent, mutated_child, elite) # list of Parent()
        #print("population: ", population)
        theBestOne = chooseBestOne(population) # Parent()
        theBestFitness = float(theBestOne.getFitness())

        ### Plotting
        drawPlot(xlist, ylist, count, theBestFitness)

        print("THE BEST of GENERATION #{0}: {1}".format(count, theBestFitness))
    while True:
        plt.pause(0.05)
    solution = parentToInt(theBestOne)
    createCSV(solution)

    prob_open.close()
    return 1






if __name__ == "__main__":
    main()


'''
def func(li):
    for i in li:
        index = getIndexList(li, i)
        a = li[-(index+1)]
        print(a)
    return 1
    

if __name__ == "__main__":
    func([1, 2, 3, 4, 5])
    func([1, 2, 3, 4])
'''