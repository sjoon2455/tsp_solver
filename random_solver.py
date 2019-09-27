#coding: utf-8
import sys
import random

def rand_createCSV(len):
    #len = len(arg)
    csv = open('solution.csv', 'w')
    l = list(range(1, len+1))
    random.shuffle(l)
    for i in range(len):
        data = l[i]
        csv.write(str(data)+"\n")
    return csv

def main():
    prob = sys.argv[1]
    prob_open = open(prob, 'r')

    lines = prob_open.readlines()
    len = lines[3]
    num = int(len[12:])
    #print(int(num))
    rand_createCSV(num)

    prob_open.close()    

main()