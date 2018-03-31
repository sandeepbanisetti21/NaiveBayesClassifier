import json
import sys
import re
from pprint import pprint

TRUE = 'True'
FAKE = 'Fake'
POSITIVE = 'Pos'
NEGATIVE = 'Neg'

nbProbs = {}
prior = {}
stopWords = []
output = []

# read file and get lines
def readDoc(file):
    with open(file, encoding="utf8") as f:
        inputlines = f.readlines()
    return inputlines

# divide json to different parts
def transformJsonData(data):
    global nbProbs
    global prior
    global stopWords
    nbProbs = data['Probabilities']
    stopWords = data['StopWords']
    prior = data['Prior']

# classify each line
def naivebayesClassify(line):
    words = tokenize(line)
   
    trueProb = prior[TRUE]
    fakeProb = prior[FAKE]
    posProb = prior[POSITIVE]
    negProb = prior[NEGATIVE]

    trainedWords = nbProbs.keys()
    truefake = TRUE
    posneg = POSITIVE

    id = words[0]

    for word in words[1:]:
        word = word.lower()
        if(word not in stopWords):
            if(word in trainedWords):
                trueProb = trueProb + nbProbs[word][TRUE]
                fakeProb = fakeProb + nbProbs[word][FAKE]
                posProb = posProb + nbProbs[word][POSITIVE]
                negProb = negProb + nbProbs[word][NEGATIVE]

    if(trueProb >= fakeProb):
        truefake = TRUE
    else:
        truefake = FAKE

    if(posProb >= negProb):
        posneg = POSITIVE
    else:
        posneg = NEGATIVE

    constructOutput(id,truefake,posneg)    

#implement several tokenize methods like lower casing, remove punctuation etc
def tokenize(line):
    #line = line.lower()
    line = re.sub('[!.:;()\[\],]', '', line)
    words = line.strip().split(" ")
    return words

# adding id and truefake class and posneg class
def constructOutput(id, truefake, posneg):
    ans = id+' '+truefake+' '+posneg
    output.append(ans)

# writing output to file
def writeOutput():
    file = open('nboutput.txt', 'w', encoding='utf-8')
    for item in output:
      file.write("%s\n" % item)

# driver function
def main():
    data = json.load(open('nbmodel.txt', encoding='utf-8'))
    transformJsonData(data)
    lines = readDoc(sys.argv[1])
    for line in lines:
        naivebayesClassify(line)
    writeOutput()

#function to run from eval
def run(filename):
    data = json.load(open('nbmodel.txt', encoding='utf-8'))
    transformJsonData(data)
    lines = readDoc(filename)
    for line in lines:
        naivebayesClassify(line)
    writeOutput() 


if __name__ == '__main__':
    main()
