import json
import sys
from pprint import pprint
from collections import defaultdict
import math
import re

#constants
TRUE = 'True'
FAKE = 'Fake'
POSITIVE = 'Pos'
NEGATIVE = 'Neg'
COUNT = 'count'

#to stores counts and a particular word count
countMap = defaultdict(lambda: defaultdict(int))

#to store a probabilities finally changed as json
nbProbs = defaultdict(lambda: defaultdict(float))

#list of stopwords store these in the json
stopwords = []

#total count of words
totalWords = 0

#driver function
def main():
    filename = sys.argv[1]    
    listOfStrings = readFile(filename)
    caluclateCount(listOfStrings)
    handleStopWords()
    doSmoothing()
    calculateProbabilities()
    writeToFile()


#read file and return the file as list of string
def readFile(filename):
    with open(filename,encoding='utf8') as f:
        inputlines = f.readlines()
    return inputlines    

#caluclate the counts of positives and negaitives and write the counts
#may store in hashmap with word as key and store
#true, fake, positive, negative
#count of a certain thing occured in corpus
def caluclateCount(strings):
    global totalWords
    for line in strings:
       tokenizedWords = tokenize(line)
       trueFake = tokenizedWords[1]
       posNeg = tokenizedWords[2]
       for word in tokenizedWords[3:]:
           countMap[word][trueFake] += 1
           countMap[word][posNeg] +=1
           countMap[word][COUNT] +=1
           totalWords +=1 
    pprint(countMap)

#implement several tokenize methods like lower casing, remove punctuation etc
def tokenize(line):
    line = re.sub('[!.:;()\[\],]', '', line)
    words = line.strip().split(" ")
    return words

#Handle the stop words like I, the,etc and mainitan a stop word list
def handleStopWords():
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