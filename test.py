import re

def main():
    line = "064BmtQ Fake Neg I was very disappointed with this hotel."
    words = tokenize(line)
    #print(words[3:])
    for word in words[3:]:
        print(word)

def tokenize(line):
    print(line)
    line = re.sub('[!.:;()\[\],]', '', line)
    words = line.strip().split(" ")
    return words

if __name__ == '__main__':
    main()    