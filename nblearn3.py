import json
import sys
from pprint import pprint
from collections import defaultdict
import math

TRUE = 'True'
FAKE = 'Fake'
POSITIVE = 'Pos'
NEGATIVE = 'Neg'

countMap = defaultdict(lambda: defaultdict(int))
nbProbs = defaultdict(lambda: defaultdict(float))

#driver function
def main():
    filename = sys.argv[1]    
    listOfStrings = readFile(filename)
    caluclateCount(listOfStrings)
    doSmoothing()
    calculateProbabilities()
    writeToFile()


#read file and return the file as list of string
def readFile(filename):
    with open(filename,encoding='utf8') as f:
        inputlines = f.readlines
    return inputlines    

#caluclate the counts of positives and negaitives and write the counts
#may store in hashmap with word as key and store
#true, fake, positive, negative
#count of a certain thing occured in corpus
def caluclateCount(listOfStrings):
    return []

#smoothing function
def doSmoothing():
    return []

#calculate the probabalities. Store it in hash map with exact format as count
#without the count
def calculateProbabilities():
    return []

#write to file called nbmodel.txt
def writeToFile():
    return []    


if __name__ == '__main__':
    main()