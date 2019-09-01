import re
import sys
from fnv import *
import uuid
import datetime
import numpy as np

x = 0.6
s = 14
r = 6
p = 15373875993579943603

lWordCount = {}
hashTable = []
wordToIntDict = {}
jSimData = {}

def wordToInt (word):
    if not (wordToIntDict.get(word)):
        wordToIntDict[word] = hash(word.encode('utf-8'), bits=64)
    return wordToIntDict[word]


def hashFunc (x, a, b, round):
    wordID = (a * x + b) % p
    return wordID


def randomNumber():
    rand64 = uuid.uuid4().int & (1 << 64) - 1
    return rand64


def jaccardSimFunc (file_path):
    file_path.rstrip('_')
    outputFile = open("question_sim_" + file_path.split('_')[1].split(".")[0] + ".tsv", "a")
    outputFile.write("qid\tsimilar-qids\n")

    canPairs = {}

    for htKey in range(0, len(hashTable)):
        for simQidsKey in hashTable[htKey]:
            simQids = hashTable[htKey][simQidsKey]
            for i in range(0, len(simQids)):
                for j in range(i + 1, len(simQids)):
                    q1 = simQids[i]
                    q2 = simQids[j]

                    pair = str(q1)+','+str(q2)
                    if pair in canPairs:
                        continue
                    else:
                        canPairs[pair] = [q1, q2]

    for pair in canPairs:
        q1 = canPairs[pair][0]
        q2 = canPairs[pair][1]

        if q1 in jSimData:
            if q2 in jSimData[q1]:
                continue
        if q2 in jSimData:
            if q1 in jSimData[q2]:
                continue

        intersect = 0
        union = lWordCount[q1][2] + lWordCount[q2][2]

        for word in lWordCount[q2][1]:
            if word in lWordCount[q1][1]:
                intersect = intersect + lWordCount[q1][1][word]
                intersect = intersect + lWordCount[q2][1][word]
        if (intersect / union >= x):
            if not q1 in jSimData:
                jSimData[q1] = []
            jSimData[q1].append(q2)
            if not q2 in jSimData:
                jSimData[q2] = []
            jSimData[q2].append(q1)

    for qid in jSimData:
        outputFile.write(qid + '\t')
        for simQid in range(0, len(jSimData[qid])):
            if (simQid + 1 == len(jSimData[qid])):
                outputFile.write(jSimData[qid][simQid])
            else: 
                outputFile.write(jSimData[qid][simQid] + ',')
        outputFile.write("\n")


def minHash (file_path):
    file = open(file_path, encoding="utf-8")

    questionLine = [line.rstrip('\n') for line in file]
    questions = {}
    for question in questionLine:
        qSplit = question.split('\t')
        if (re.match('^[0-9]+$', qSplit[0])): 
            if (len(qSplit) == 2):
                questions[qSplit[0]] = qSplit[1]
            else:
                questions[qSplit[0]] = ''

    qidWords = {}

    for qid in questions:
        wordCount = {}
        text = questions[qid]
        jSimData[qid] = []
        tSplit = text.split(' ')

        for i in range(0, len(tSplit)):
            if not (re.match('^[0-9a-zA-Z]*$', tSplit[i])): 
                tSplit[i] = re.sub('[\\?\\.\\!\\<\\>\\,\\\\\\;\\\'\\:\\"\\[\\]\\{\\}\\@\\#\\$\\%\\^\\&\\*\\(\\)\\`\\_\\=\\+\\-]*', '', tSplit[i])
            tSplit[i] = tSplit[i].lower()

            if tSplit[i] in wordCount:
                wordCount[tSplit[i]] += 1
            else:
                wordCount[tSplit[i]] = 1
        lWordCount[qid] = (
            qid, wordCount, len(tSplit)
        )

        qidWords[qid] = tSplit

    for htKey in range(0, len(hashTable)):
        a = []
        b = []
        for qid in qidWords:
            for i in range(0, r): 
                a.append(randomNumber())
                b.append(randomNumber())

            minHash = []
            for i in range(0, r):
                hashList = []
                for word in qidWords[qid]:
                    tempWordID = wordToInt(word)
                    wordID = hashFunc(a[i], b[i], tempWordID, i)
                    hashList.append(wordID)
            
                minHash.append(min(hashList))
            key = "" + str(minHash[0]) + "" + str(minHash[1]) + "" + str(minHash[2]) + "" + str(minHash[3]) + "" + str(minHash[4]) + "" + str(minHash[5]) + ""

            if key in hashTable[htKey]:
                hashTable[htKey][key].append(qid)
            else:
                hashTable[htKey][key] = []
                hashTable[htKey][key].append(qid)

    wordToIntDict = 0
    qidWords = 0
    questions = 0
    file.close()

if not (len(sys.argv) == 2):
    print('ERROR: Missing arguments')
    print('\tpython minHash.py [.tsv filename]')
else:

    for j in range(0, s):
        hashTable.append({})
    
    print('computing minHash signatures...')
    print(datetime.datetime.now())

    minHash(sys.argv[1])

    print('... finished minHash signatures')
    print(datetime.datetime.now())

    print('computing jaccard similarities on canidate pairs...') 
    print(datetime.datetime.now())
    jaccardSimFunc(sys.argv[1])

    print('... completed minhashing with local sensitivity hashing')
    print(datetime.datetime.now())