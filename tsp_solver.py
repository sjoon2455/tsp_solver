# coding: utf-8
import sys
import random
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

def initialPopulation()
def select()
def getFitness()
def crossover()
def mutate()


### main function
### input: -
### output: .csv
def main():
    prob = sys.argv[1]
    prob_open = open(prob, 'r')

    lines = prob_open.readlines()
    len = lines[3]
    num = int(len[12:])
    #print(int(num))
    rand_createCSV(num)

    prob_open.close()    

#main()