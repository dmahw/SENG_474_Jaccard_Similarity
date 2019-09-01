import re
import sys

def jaccardSim (file_path):
    file = open(file_path, encoding="utf8")

    questionLine = [line.rstrip('\n') for line in file]
    questions = {}
    for question in questionLine:
        qSplit = question.split('\t')
        if (re.match('^[0-9]+$', qSplit[0])): 
            if (len(qSplit) == 2):
                questions[qSplit[0]] = qSplit[1]
            else:
                # print('ERROR: Found an error in the file')
                questions[qSplit[0]] = ''
        # else:
        #     print('ERROR: Invalid Question ID >>> ' + qSplit[0])

    # qid: list of words
    lWordCount = []
    for qid in questions:
        wordCount = {}
        text = questions[qid]
        tSplit = text.split(' ')
        for word in tSplit:
            if not (re.match('^[0-9a-zA-Z]*$', word)): 
                word = re.sub('[\\?\\.\\!\\<\\>\\,\\\\\\;\\\'\\:\\"\\[\\]\\{\\}\\@\\#\\$\\%\\^\\&\\*\\(\\)\\`\\_\\=\\+\\-]*', '', word)
            if word.lower() in wordCount:
                wordCount[word.lower()] += 1
            else:
                wordCount[word.lower()] = 1
        lWordCount.append((
            qid, wordCount, len(tSplit)
        ))

    jaccardSim = {}

    file_path.rstrip('_')
    outputFile = open("question_sim_" + file_path.split('_')[1].split(".")[0] + ".tsv", "a")
    outputFile.write("qid\tsimilar-qids\n")

    for in1 in range(0, len(lWordCount)):
        outputFile.write(lWordCount[in1][0] + "\t")
        # print(lWordCount[in1][0], end="\t")

        if lWordCount[in1][0] not in jaccardSim:
            jaccardSim[lWordCount[in1][0]] = []

        for in2 in range(in1 + 1, len(lWordCount)):
            if lWordCount[in2][0] not in jaccardSim:
                jaccardSim[lWordCount[in2][0]] = []

            union = lWordCount[in1][2] + lWordCount[in2][2]
            intersect = 0
            for word in lWordCount[in2][1]:
                if word in lWordCount[in1][1]:
                    intersect += lWordCount[in1][1][word]
                    intersect += lWordCount[in2][1][word]
            if (intersect / union >= 0.6):
                jaccardSim[lWordCount[in1][0]].append(lWordCount[in2][0])
                jaccardSim[lWordCount[in2][0]].append(lWordCount[in1][0])
        
        for num in range(0, len(jaccardSim[lWordCount[in1][0]])):
            if (num + 1 == len(jaccardSim[lWordCount[in1][0]])):
                outputFile.write(jaccardSim[lWordCount[in1][0]][num])
                # print(jaccardSim[lWordCount[in1][0]][num], end='')
            else:
                outputFile.write(jaccardSim[lWordCount[in1][0]][num] + ',')
                # print(jaccardSim[lWordCount[in1][0]][num], end=',')
        outputFile.write("\n")
        # print('\n', end='')

if not (len(sys.argv) == 2):
    print('ERROR: Missing arguments')
    print('\tpython jaccardSimilarity.py [.tsv filename]')
else:
    jaccardSim(sys.argv[1])
