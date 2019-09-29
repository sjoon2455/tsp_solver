# coding: utf-8
import sys
import random
import datetime
import time
from cityClass import City
from parentClass import Parent
from geneIndexClass import GeneIndex
from printPretty import printPretty


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
def parentToInt(solution):
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
def breed(dad, mom, r):
    crossover_cities = []
    dadRoute = dad.getList()
    momRoute = mom.getList()
    index = 0
    #type check necessary
    for i in dadRoute:
        if isPicked(i, r):
            a = GeneIndex(i, index)
            crossover_cities.append(a)
            index = getIndexList(momRoute, i)
            momRoute[index] = 0
        index += 1
    for j in crossover_cities:
        momRoute[j.getIndex()] = j.getNum()
    child = Parent(momRoute, 0)
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
        while(len(parents) != 1):
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
    printPretty("Generating intial population...")
    population = []
    alignedList = list(range(1, num+1))
    # generate random permutated lists
    count = 0
    while count < pop:
        random.shuffle(alignedList) # not aligned anymore
        population.append(alignedList)
        count += 1
        
    
    for route in population: # route: list of int
        fitness = computeFitness(route, cities)
        parent = Parent(route, fitness)
        population.remove(route)
        population.append(parent)

    printPretty("Generated intial population")
    return population



### calculate fitness: total distance between cities
### input: list of int, list of City()
### output: int
def computeFitness(route, cities):
    printPretty("Computing Fitness...")
    distance = 0
    #print(route)
    #routeList = route.getList()
    #actualRoute = [cities[i-1] for i in routeList] # list of City()
    actualRoute = [cities[i-1] for i in route] # list of City()
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
    printPretty("Sampled using SUS")
    return selected

### Make pairs of Parent()s, randomly and uniformly pick some part and switch the same number sequence retaining its orders
### input: list of Parent(), crossover rate(0~1.0), total population int
### output: list of Parent()
def orderedCrossover(selected, r, pop):
    printPretty("Crossovering...")
    childs = []
    numChild = 0
    numPop = int(0.5*pop if pop%2==0 else 0.5*pop+1)
    #print(numPop) # 6
    while numChild < numPop:
        #print("SELECTED: ", selected)
        pairs = makePair(selected)
        for pair in pairs:
            numChild += 1
            print(numChild)
            child = breed(pair[0], pair[1], r)
            childs.append(child)
    printPretty("Crossovered")
    return childs

    

### with some probability r, swap two cities
### input: list of Parent(), probability r(0~1.0)
### output: list of Parent()
def mutate(crossovered, r):
    printPretty("Mutating...")
    for parent in crossovered:
        li = parent.getList()
        #print("getlist: ", li)
        mutated_li = mutateIndividual(li, r)
        parent.setList(mutated_li)
    printPretty("Mutated")
    return crossovered



### update fitness for each Parent()
### input: list of Parent()
### output: list of Parent()
def updateFitness(parents, cities):
    printPretty("Updating fitness of the mutated...")
    for parent in parents:
        fit = computeFitness(parent.getList(), cities)
        parent.setFitness(fit)
    printPretty("Updated fitness of the mutated")
    return parents


### maintain M best from Parents, get rid of M worst from Child
### input: list of Parent(), list of Parent(), percentage of elite(0~1.0)
### output: list of Parent()
def chooseBestGeneration(parent, child, m):
    printPretty("Choosing the best generation...")
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
    printPretty("Chose the best generation")
    return best




### choose the best fitness Parent() among Parent()s
### input: list of Parent()
### output: Parent()
def chooseBestOne(pop):
    printPretty("Choosing the best one...")
    res = pop[0]
    for parent in pop:
        if parent.getFitness() > res.getFitness():
            res = parent
    printPretty("Chose the best one")
    return res


### given list of int with city indices, create csv file
### input: list of int
### output: .csv with single column city indices
def createCSV(arg):
    printPretty("Creating CSV file...")
    len = len(arg)
    csv = open('solution_{0}.csv'.format(str(datetime.datetime.now().time())[:-7]), 'w')
    for i in range(len):
        data = arg[i]
        csv.write(data)
    printPretty("Created CSV file")
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

    # main loop
    count = 0
    population = initialPop
    while count < loop:
        count += 1
        selected = []
        sum = sumFitness(parents)
        parents = computeFPS(parents, sum)
        print("fps computed: ", parents)
        selected_parent = sampleSUS(parents, int(0.5*pop))
        print("sus computed: ", selected_parent)
        crossovered_child = orderedCrossover(selected_parent, crossoverRate, pop)
        print("crossovered: ", crossovered_child)
        mutated_parent = mutate(selected_parent, mutationRate)
        print("mutated parent: ", mutated_parent)
        mutated_child = mutate(crossovered_child, mutationRate)
        print("mutated child: ", mutated_child)
        mutated_parent = updateFitness(mutated_parent, cities)
        mutated_child = updateFitness(mutated_child, cities)
        population = chooseBestGeneration(mutated_parent, mutated_child, elite) # list of Parent()
        print("population: ", population)
        theBestOne = chooseBestOne(population) # Parent()
        theBestFitness = float(theBestOne.getFitness())
        print("THE BEST of GENERATION #{0}: {1}".format(count, theBestFitness))
    solution = parentToInt(theBestOne)
    createCSV(solution)

    prob_open.close()
    return 1

if __name__ == "__main__":
    main()


'''
if __name__ != "__main__":
''' 