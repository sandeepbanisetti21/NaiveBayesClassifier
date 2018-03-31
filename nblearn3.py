import json
import sys
from pprint import pprint
from collections import defaultdict
import math
import re

# constants
TRUE = 'True'
FAKE = 'Fake'
POSITIVE = 'Pos'
NEGATIVE = 'Neg'
COUNT = 'count'

# to stores counts and a particular word count
countMap = defaultdict(lambda: defaultdict(int))

# to store a probabilities finally changed as json
nbProbs = defaultdict(lambda: defaultdict(float))

# list of stopwords store these in the json
stopwords = ['hers', "it's", 'too', 'who', 'he', "won't", 'then', 'up', 'between', 'ma', 'whom', 'over', 'theirs', 'on', 'just', 'isn', 'while', "don't", 'shan', "shan't", "that'll", 'their', 'does', 'yourself', 'if', 'of', 'to', 'most', 'down', 'off', "doesn't", "you'll", 'such', 's', 'will', 'under', 'its', 'mightn', 'ours', 'not', 'into', 'ourselves', 'me', 'few', 'below', 'own', 'weren', "haven't", "didn't", "aren't", 'the', 'during', 'my', 'a', 've', 'through', 'and', 'can', 'yourselves', 'ain', "wouldn't", "you'd", 'once', 'should', "wasn't", 'above', 'her', 'at', 'she', 'has', 't', 're', 'yours', 'him', "she's", 'have', 'been', 'i', 'themselves', 'so', 'again', 'll', 'with', 'himself', 'there', 'y', 'it', 'his', 'be', 'or',
             'don', 'each', 'itself', 'that', 'didn', 'until', 'from', 'won', 'being', 'how', 'you', 'now', 'other', 'is', 'some', 'are', 'same', 'very', "hasn't", 'haven', 'o', 'hadn', 'any', 'against', "couldn't", 'this', 'having', 'in', 'shouldn', 'those', 'what', 'because', 'them', 'mustn', "shouldn't", 'was', 'did', 'here', 'all', 'herself', "should've", 'd', "hadn't", "mustn't", "you've", 'doesn', "isn't", 'needn', 'our', 'further', 'were', 'why', "you're", 'nor', 'myself', 'm', 'aren', 'wasn', 'doing', 'these', "needn't", "mightn't", 'by', 'about', 'more', 'only', 'couldn', 'wouldn', 'before', 'they', "weren't", 'where', 'which', 'do', 'when', 'no', 'as', 'an', 'am', 'both', 'hasn', 'had', 'your', 'out', 'than', 'we', 'after', 'for', 'but']

# total count of words
tagCount = defaultdict(int)

# priorProbabilityCounter
priorpCounter = defaultdict(int)

# priorProbability
priorProbability = defaultdict(float)

# driver function


def main():
    filename = sys.argv[1]
    listOfStrings = readFile(filename)
    caluclateCount(listOfStrings)
    handleStopWords()
    doSmoothing()
    calculatePriorProbabilities()
    calculateProbabilities()
    writeToFile()

# function to run from eval


def run(filename):
    listOfStrings = readFile(filename)
    caluclateCount(listOfStrings)
    handleStopWords()
    doSmoothing()
    calculatePriorProbabilities()
    calculateProbabilities()
    writeToFile()


# read file and return the file as list of string
def readFile(filename):
    with open(filename, encoding='utf8') as f:
        inputlines = f.readlines()
    return inputlines

# caluclate the counts of positives and negaitives and write the counts
# may store in hashmap with word as key and store
#true, fake, positive, negative
# count of a certain thing occured in corpus


def caluclateCount(strings):
    for line in strings:
        tokenizedWords = tokenize(line)
        trueFake = tokenizedWords[1]
        priorpCounter[trueFake] += 1
        posNeg = tokenizedWords[2]
        priorpCounter[posNeg] += 1
        for word in tokenizedWords[3:]:
            word = word.lower()
            if(word not in stopwords):
                countMap[word][trueFake] += 1
                countMap[word][posNeg] += 1
                countMap[word][COUNT] += 1
                tagCount[trueFake] += 1
                tagCount[posNeg] += 1
                tagCount[COUNT] += 1
    # pprint(countMap)

# implement several tokenize methods like lower casing, remove punctuation etc


def tokenize(line):
    #line = line.lower()
    line = re.sub('[!.:;()\[\],\",\']', '', line)
    words = line.strip().split(" ")
    return words

# Handle the stop words like I, the,etc and mainitan a stop word list


def handleStopWords():
    return []

# smoothing function


def doSmoothing():
    # print('-------------------------------------------------------------------------------------------------------------------------------')
    for k in countMap.keys():
        countMap[k][TRUE] += 1
        countMap[k][FAKE] += 1
        countMap[k][POSITIVE] += 1
        countMap[k][NEGATIVE] += 1
    # pprint(countMap)

# calculatePriorProbabilities


def calculatePriorProbabilities():
    pprint(priorpCounter)
    priorProbability[TRUE] = math.log10(
        priorpCounter[TRUE]/(priorpCounter[TRUE]+priorpCounter[FAKE]))
    priorProbability[FAKE] = math.log10(
        priorpCounter[FAKE]/(priorpCounter[TRUE]+priorpCounter[FAKE]))
    priorProbability[POSITIVE] = math.log10(
        priorpCounter[POSITIVE]/(priorpCounter[POSITIVE]+priorpCounter[NEGATIVE]))
    priorProbability[NEGATIVE] = math.log10(
        priorpCounter[NEGATIVE]/(priorpCounter[POSITIVE]+priorpCounter[NEGATIVE]))


# calculate the probabalities. Store it in hash map with exact format as count
# without the count
def calculateProbabilities():
    uniqueWords = len(countMap.keys())
    smoothedTrueWords = tagCount[TRUE]+uniqueWords
    smoothedFakeWords = tagCount[FAKE]+uniqueWords
    smoothedPosWords = tagCount[POSITIVE]+uniqueWords
    smoothedNegWords = tagCount[NEGATIVE]+uniqueWords
    for k in countMap.keys():
        nbProbs[k][TRUE] = math.log10(countMap[k][TRUE]/smoothedTrueWords)
        nbProbs[k][FAKE] = math.log10(countMap[k][FAKE]/smoothedFakeWords)
        nbProbs[k][POSITIVE] = math.log10(
            countMap[k][POSITIVE]/smoothedPosWords)
        nbProbs[k][NEGATIVE] = math.log10(
            countMap[k][NEGATIVE]/smoothedNegWords)
    # pprint(nbProbs)

# write to file called nbmodel.txt


def writeToFile():
    data = {}
    data['Probabilities'] = nbProbs
    data['StopWords'] = stopwords
    data['Prior'] = priorProbability
    #pprint(data)
    x = json.dumps(data, ensure_ascii=False)
    with open('nbmodel.txt', 'w', encoding='utf-8') as file:
        file.write(x)


if __name__ == '__main__':
    main()
