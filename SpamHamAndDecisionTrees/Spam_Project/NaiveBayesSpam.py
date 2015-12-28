__author__ = 'mahathi'
from collections import defaultdict
import math
import sys

# Feature selection for spam
# Number of special characters
# Junk email does not contain attachments
# Time of email. mostly at night
# .edu can never be a junk mail
# More capital letters and money

# compute the probability
def computeProbability(probabilityList):
    sumProb = 0
    for probability in probabilityList:
        sumProb = sumProb + math.log(1-probability) - math.log(probability)

    if sumProb > 700:
        return 0;
    totalProbability =  (1/(1+ math.exp(sumProb)))

    return totalProbability

if __name__ == '__main__':
    print("Reading the test data....")

    smoothingtechnique = sys.argv[1]
    trainFile = sys.argv[2]
    testFile = sys.argv[3]
    publicCorpus = 1


    # Read the input file
    #C:/Users/mahathi/PycharmProjects/Spam_Detection/train

    trainingDataFile = open(trainFile, 'r')

    if ("public" in trainFile):
        publicCorpus = 1

    content = trainingDataFile.readlines()

    SpamBagOfWords = defaultdict(int)
    HamBagOfWords = defaultdict(int)

    for line in content:
        tokens = line.split(" ")

        # check if this line refers to ham or spam
        isSpam = 0
        classifier = tokens[1]
        if classifier == "spam":
            isSpam = 1

        i = 2
        # add the tokens into respective bags
        while i < len(tokens):
            if isSpam:
                SpamBagOfWords[tokens[i]] = SpamBagOfWords[tokens[i]] + int(tokens[i + 1])
            else:
                HamBagOfWords[tokens[i]] = HamBagOfWords[tokens[i]] + int(tokens[i + 1])

            i = i + 2;


    # we have read the training data

    # now apply the training data on the test set
    # test File C:/Users/mahathi/PycharmProjects/Spam_Detection/test
    testDataFile = open(testFile, 'r')
    testContent = testDataFile.readlines()

    correctResult = 0
    totalResult = 0
    for line in testContent:
        SpamprobabilityList = []
        HamProbabilityList = []
        tokens = line.split(" ")

        expectedResult = tokens[1]
        i = 2
        while i < len(tokens):
            # check the frequency
            numWordsInSpam = SpamBagOfWords[tokens[i]]
            numWordsInHam = HamBagOfWords[tokens[i]]

            # apply smoothing techniques
            if numWordsInSpam == 0 or numWordsInHam == 0:
                if smoothingtechnique == "1":
                    numWordsInSpam = numWordsInSpam + 1
                    numWordsInHam = numWordsInHam + 1
                if smoothingtechnique == "0":
                    i = i + 2
                    continue
                if smoothingtechnique == "2":
                    #weighted smoothing
                    numWordsInSpam = (numWordsInSpam + 1 ) * 0.25
                    numWordsInHam = (numWordsInHam + 1) * 0.75

            # apply algorithm
            spamProb = numWordsInSpam/(numWordsInSpam + numWordsInHam)
            hamProb = numWordsInHam/(numWordsInSpam + numWordsInHam)
            j = 0;
            while j < int(tokens[i + 1]):
                SpamprobabilityList.append(spamProb)
                HamProbabilityList.append(hamProb)
                j =  j + 1

            i = i + 2

        # now check the complete probability
        if SpamprobabilityList.__len__() == 0:
            continue;
        totalSpamProbability = computeProbability(SpamprobabilityList)
        totalHamProbability = computeProbability(HamProbabilityList)
        if totalSpamProbability > totalHamProbability:
            print("probably spam")
            actualResult = "spam"

        else:
            print("probably legit")
            actualResult = "ham"

        if expectedResult.__eq__(actualResult):
            correctResult = correctResult + 1

        totalResult = totalResult + 1

    percentageAccuracy = (correctResult/totalResult) * 100
    print("Accurancy Percentage :" + str(percentageAccuracy))














