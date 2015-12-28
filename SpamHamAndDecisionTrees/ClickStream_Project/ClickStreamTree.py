__author__ = 'mahathi'
import csv
import math
import sys
from collections import namedtuple
from heapq import heappush, heappop

class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

# degrees of freedom : 1 because we are splitting the outcomes into half
# for p = 0.05 = 3.841
# for p = 0.01 = 6.635
# for p = 1 = 2.706

Node = namedtuple("Node", "featureIndex, min, mid, max")
InfoGainNode = namedtuple("InfoGainNode", "infogain, featureIndex, min, mid, max, leftTreeInfoGain, rightTreeInfoGain")
attributeNodes = []
DecisionTree = []
ThresholdValueDepth = [50,150,260]

if __name__ == '__main__':
    print("Reading the input files and generating a tree....")

trainingData = []
noOfRows = 0

# training file is : C:/Users/mahathi/PycharmProjects/ClickStream/trainfeat.csv
trainingFile = sys.argv[2]
f = open(trainingFile,'r')
reader = csv.reader(f)
for row in reader:
    rowData = row[0]
    dataCols = rowData.split(" ")
    trainingData.append(dataCols)
    noOfRows = noOfRows + 1

noOfFeatures = len(trainingData[10])

for i in range(0,noOfRows):
    for j in range(0,noOfFeatures):
        trainingData[i][j] = int(trainingData[i][j])


# testlabs : C:/Users/mahathi/PycharmProjects/ClickStream/trainlabs.csv
resultFile = sys.argv[3]
f2 = open(resultFile,'r')
reader = csv.reader(f2)
trainingResult = []

for row in reader:
    rowData = row[0]
    trainingResult.append(int(rowData))


#Find out the feature which has the low entropy

#overall entropy of system

totalProb = noOfRows
noofYes = 0
for i in range(0,noOfRows):
    if trainingResult[i] == 1:
        noofYes = noofYes + 1

noofNo = totalProb - noofYes

totalEntropy = -((noofYes/totalProb)* math.log2(noofYes/totalProb)) - ((noofNo/totalProb) * math.log2(noofYes/totalProb))
expectedYes = (noofYes/totalProb)
expectedNo = (noofNo/totalProb)

#for every feature, split the values and calculate the entropy

for i in range(0,noOfFeatures):
    min = trainingData[0][i]
    max = trainingData[0][i]
    for j in range(0,noOfRows):

        if trainingData[j][i] < min:
            min = trainingData[j][i]

        if trainingData[j][i] > max:
            max = trainingData[j][i]

    # I have now min and max. Now divide the values
    mid = math.ceil(max/2)
    tnode = Node(i, min, mid, max)
    #print(i)
    attributeNodes.append(tnode)
    # min to mid
    # mid to max

informationGain = 0
maxInformationGainIndex = 0
for node in attributeNodes:
    nmin = node.min
    nmax = node.max
    nmid = node.mid
    nfeatureIndex = node.featureIndex

    firstyes = 0
    firstno = 0
    secondyes = 0
    secondno = 0
    e1 = 0
    e2 = 0

    for k in range(0,noOfRows):
        if trainingData[k][nfeatureIndex] in range(nmin-1,nmid):
            if trainingResult[k] == 1 :
                firstyes = firstyes + 1
            else:
                firstno = firstno + 1

        if trainingData[k][nfeatureIndex] in range(nmid,nmax + 1):
            if trainingResult[k] == 1 :
                secondyes = secondyes + 1
            else:
                secondno = secondno + 1

    if nmin != nmid:
        e1 = -((firstyes/(firstyes + firstno))* math.log2(firstyes/(firstyes + firstno))) - (firstno/(firstyes + firstno) * math.log2(firstno/(firstyes + firstno)))
    if nmid != nmax:
        e2 = -((secondyes/(secondyes + secondno))* math.log2(secondyes/(secondyes + secondno))) - (secondno/(secondyes + secondno) * math.log2(secondno/(secondyes + secondno)))

    #observedYes = firstyes/(firstyes + firstno) + secondyes/(secondyes + secondno)
    #observedNo = secondno/(secondyes + secondno) + firstno/(firstyes + firstno)

    currinformationGain = totalEntropy - (e1*((firstyes + firstno)/totalProb)) - (e2*((secondyes + secondno)/totalProb))
    if currinformationGain > informationGain:
        informationGain = currinformationGain
        maxInformationGainIndex = nfeatureIndex
        #infogain featureIndex, min, mid, max
    nodeElement = InfoGainNode(infogain = -currinformationGain, featureIndex = nfeatureIndex, min = nmin, mid = nmid, max = nmax, leftTreeInfoGain = e1, rightTreeInfoGain = e2)
    heappush(DecisionTree,nodeElement)

print(maxInformationGainIndex)
print(DecisionTree)

#Read the test file
testData = []
testrows = 0
#testfeature file
trainingFile = sys.argv[4]
f = open(trainingFile,'r')
reader = csv.reader(f)
for row in reader:
    rowData = row[0]
    dataCols = rowData.split(" ")
    testData.append(dataCols)
    testrows = testrows + 1

for i in range(0,testrows):
    for j in range(0,noOfFeatures):
        testData[i][j] = int(testData[i][j])

#Now iterate over each test row
# threshold value for 150 depth tree

resultFile = sys.argv[5]
f2 = open(resultFile,'r')
reader = csv.reader(f2)
testResult = []

for row in reader:
    rowData = row[0]
    testResult.append(int(rowData))

DecisionNode = None
ThresholdValueIndex = 0
print(sys.argv[1])
if sys.argv[1] == "0.01":
    print("inside this")
    DecisionNode = DecisionTree[ThresholdValueDepth[0]]
    ThresholdValueIndex = 0
if sys.argv[1] == "0.05":
    DecisionNode = DecisionTree[ThresholdValueDepth[1]]
    ThresholdValueIndex = 1
if sys.argv[1] == "1.00":
    DecisionNode = DecisionTree[ThresholdValueDepth[2]]
    ThresholdValueIndex = 2

correctDecisions = 0

for i in range(0,testrows):
    clickCount = testData[i][ThresholdValueDepth[ThresholdValueIndex]]
    result = 0
    if clickCount in range(DecisionNode.min, DecisionNode.mid):
        if DecisionNode.leftTreeInfoGain > DecisionNode.rightTreeInfoGain:
            result = 1
        else:
            result = 0
    else:
        if DecisionNode.leftTreeInfoGain < DecisionNode.rightTreeInfoGain:
            result = 1
        else:
            result = 0
    #print(result)
    #print(testResult[i])
    if result == testResult[i]:
        correctDecisions = correctDecisions + 1


percentageCorrect = (correctDecisions/testrows) * 100

print("Percentage Accuracy :" + str(percentageCorrect))
print("done")



