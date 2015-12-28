__author__ = 'mahathi'

from array import *
from collections import namedtuple
from random import randint
from heapq import heappush, heappop
import copy
from sys import getsizeof
from datetime import datetime

# This the board representation. All moves are represented from their corresponding board number
PEGSOLITAIREBOARD = []
PEGSOLITAIREBOARD.append(['x', 'x', 0, 1, 2, 'x', 'x'])
PEGSOLITAIREBOARD.append(['x', 'x', 3, 4, 5, 'x', 'x'])
PEGSOLITAIREBOARD.append([6,7, 8, 9, 10, 11, 12])
PEGSOLITAIREBOARD.append([13,14, 15, 16, 17, 18, 19])
PEGSOLITAIREBOARD.append([20,21, 22, 23, 24, 25, 26])
PEGSOLITAIREBOARD.append(['x', 'x', 27, 28, 29, 'x', 'x'])
PEGSOLITAIREBOARD.append(['x', 'x', 30, 31, 32, 'x', 'x'])

#This is a heuristic. Every filled peg in a board is assigned its corresponding weight on the board
PAGODAHEURISTIC = []
PAGODAHEURISTIC.append([5,5,3,3,3,5,5])
PAGODAHEURISTIC.append([5,5,0,0,0,5,5])
PAGODAHEURISTIC.append([3,0,2,0,2,0,3])
PAGODAHEURISTIC.append([3,0,0,0,0,0,3])
PAGODAHEURISTIC.append([3,0,2,0,2,0,3])
PAGODAHEURISTIC.append([5,5,0,0,0,5,5])
PAGODAHEURISTIC.append([5,5,3,3,3,5,5])


# The elements that are pushed to the stack are of this form
GameStackElement = namedtuple("GameStackElement", "fromPoint toPoint")

#this is a minimum priority queue element.
GameQueueElement = namedtuple("GameQueueElement", "heuristicValue toBeFilled  jumpedOver currPosition direction")

# denotes a specific index of the game board.
Point = namedtuple("Point", "xordinate yordinate")

# For tracking memory usage
memoryUsage = 0

#Number of nodes visited
numberofNodes = 0

#Number of moves made
numberofMoves = 0

#Failed nodes
failedboards = set()

class SolitaireStack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

# initialize the game stack
stack = SolitaireStack()

def printBoard(gameBoard):
    for x in range(0, 7):
        print(gameBoard[x])

#This is a heuristic. This is neither consistent or admissible
def computeHeuristic(gameBoard, currPoint, jumpedOverPoint, newPosition ):
    heuristic = randint(1,20)
    return heuristic

# The following is a heuristic that computes the sum of the  distances of every peg from the centre
def computeHeuristicManhattan(gameBoard, currPoint, jumpedOverPoint, newPosition):
    dummyboard = copy.deepcopy(gameBoard)
    #make a move
    dummyboard[newPosition.xordinate][newPosition.yordinate] = 'X'
    dummyboard[jumpedOverPoint.xordinate][jumpedOverPoint.yordinate] = '0'
    dummyboard[currPoint.xordinate][currPoint.yordinate] = '0'

    # compute heuristics for this board move
    heuristic = 0
    for i in range(0, 7):
        for j in range(0, 7):
            if isFilled(dummyboard[i][j]):
                #calculate distance from centre
                heuristic = heuristic + ((3-i) * (3-i) + (3-j) * (3-j))

    return heuristic

# Heuristic 2 : The board is assigned a heuristic after a move is made based on the position of filled pegs
def computeHeuristicPagoda(gameBoard, currPoint, jumpedOverPoint, newPosition):
    dummyboard = copy.deepcopy(gameBoard)
    #make a move
    dummyboard[newPosition.xordinate][newPosition.yordinate] = 'X'
    dummyboard[jumpedOverPoint.xordinate][jumpedOverPoint.yordinate] = '0'
    dummyboard[currPoint.xordinate][currPoint.yordinate] = '0'

    # Compute heuristics for the board using the pagoda function
    heuristic = 0
    for i in range(0, 7):
        for j in range(0, 7):
            if isFilled(dummyboard[i][j]):
                heuristic = heuristic + PAGODAHEURISTIC[i][j]

    return heuristic

def countPegs(gameBoard):
    Pegs = 0
    for x in range(0, 7):
        for y in range(0, 7):
            if gameBoard[x][y] == 'X':
                Pegs = Pegs + 1
    return Pegs;

#check if the given point in a board is a valid peg location
def isValidBoardCoordinate(x_coordinate, y_coordinate):
    if x_coordinate in range(0, 7) and y_coordinate in range(0, 7):
        return 1;
    return 0

#check if the given position in a board has a peg
def isFilled(boardCharacter):
    if boardCharacter == 'X':
        return 1
    else:
        return 0

#check if the given position in a board is vacant
def isVacant(boardCharacter):
    if boardCharacter == '0':
        return 1
    else:
        return 0

# check if we have reached the goal state or not
def goalReached(gameBoard, numberofPegs):
    if numberofPegs == 1 and gameBoard[3][3] == 'X':
        return 1
    return 0

# Play the game for the given configuration of the game, number of pegs and the depth
def playPegSolitaire(gameBoard, numberofPegs):
    global numberofNodes
    global stack
    global numberofMoves
    # check if this is a goal state
    if goalReached(gameBoard, numberofPegs):
        return 1 # we need not play if this is goal
    gameheap = []
    for i in range(0, 7):
        for j in range(0, 7):
            # for a board co-ordinate
            # for each valid move add to queue with the heuristic
            # for each board position
            if isFilled(gameBoard[i][j]):
                    # calculate all possible directions it can move
                    for direction in range(0, 4):
                        if direction == 0:  # North
                            i_1 = i - 1
                            j_1 = j
                        elif direction == 1:  # East
                            i_1 = i
                            j_1 = j + 1
                        elif direction == 2:  # West
                            i_1 = i
                            j_1 = j - 1
                        else:  # South
                            i_1 = i + 1
                            j_1 = j

                        if isValidBoardCoordinate(i_1, j_1):
                            if isFilled(gameBoard[i_1][j_1]):
                                 # now that its coordinate is filled  check with the next co-ordinate
                                if direction == 0:  # North
                                    i_2 = i_1 - 1
                                    j_2 = j_1
                                elif direction == 1:  # East
                                    i_2 = i_1
                                    j_2 = j_1 + 1
                                elif direction == 2:  # West
                                    i_2 = i_1
                                    j_2 = j_1 - 1
                                else:  # South
                                    i_2 = i_1 + 1
                                    j_2 = j_1

                                if isValidBoardCoordinate(i_2, j_2):
                                    if isVacant(gameBoard[i_2][j_2]):
                                        # Now this is a valid move
                                        # compute the heuristic for this
                                        currPoint = Point(i,j)
                                        jumpedOverPoint = Point(i_1, j_1)
                                        newPosition = Point(i_2, j_2)
                                        # We are not changing the gameboard by making moves, we just calculate the heuristic of each move
                                        heuristicValue = computeHeuristic(gameBoard, currPoint, jumpedOverPoint, newPosition )
                                        # add this node to the queue
                                        gameElement = GameQueueElement(heuristicValue = heuristicValue, toBeFilled = newPosition, jumpedOver = jumpedOverPoint, currPosition = currPoint, direction = direction)
                                        heappush(gameheap, gameElement)


    # now i have a queue , with all valid moves
    while gameheap:
        # pull out the element with the least heuristic value. This is our favourable board nearer to the goal
        gameElement = heappop(gameheap)
        gameBoard[gameElement.toBeFilled.xordinate][gameElement.toBeFilled.yordinate] = 'X'
        gameBoard[gameElement.jumpedOver.xordinate][gameElement.jumpedOver.yordinate] = '0'
        gameBoard[gameElement.currPosition.xordinate][gameElement.currPosition.yordinate] = '0'
        #play game with this
        if not failedboards.__contains__(str(gameBoard)):
            numberofPegs = numberofPegs - 1
            numberofNodes = numberofNodes + 1
            numberofMoves = numberofMoves + 1
            m = GameStackElement(fromPoint = gameElement.currPosition,toPoint = gameElement.toBeFilled )
            # push to stack
            stack.push(m)
            if playPegSolitaire(gameBoard,numberofPegs):
                return 1
            # this move did not work. try with other elements in the queue
            # before you try, undo the move
            stack.pop()
            dummyBoard = [list(x) for x in zip(*gameBoard)]
            failedboards.add(str(dummyBoard))
            numberofPegs = numberofPegs +1
            numberofMoves = numberofMoves + 1

        gameBoard[gameElement.toBeFilled.xordinate][gameElement.toBeFilled.yordinate] = '0'
        gameBoard[gameElement.jumpedOver.xordinate][gameElement.jumpedOver.yordinate] = 'X'
        gameBoard[gameElement.currPosition.xordinate][gameElement.currPosition.yordinate] = 'X'

        # none of them in the queue worked, its time to try with other peg
        # make sure you increase the number of pegs



    return 0



# Main Function
if __name__ == '__main__':

    # Get the board configuration
    pegSBoard = input(" Please enter the board configuration :")

    # ----validate(pegSBoard input)

    # remove the start and end tags
    pegSBoard = pegSBoard.replace("<", "")
    pegSBoard = pegSBoard.replace(">", "")

    boardLine = pegSBoard.split(",", 7)

    gameBoard = []

    for line in boardLine:
        lineConf = list(line)
        gameBoard.append(lineConf)

    print("Given configuration of the board is :")
    printBoard(gameBoard)

    memoryUsage = memoryUsage + getsizeof(gameBoard)

    # count total number of pegs
    numberofPegs = countPegs(gameBoard)
    print("-------------------------")
    print(" The total number of pegs are: " + str(numberofPegs))
    print("-------------------------")

    print(" Starting to generate a solution . . .\n")
    startTime = datetime.now()

    if playPegSolitaire(gameBoard, numberofPegs):
        executionTime = datetime.now() - startTime
        print("Execution time of the program: ", str(executionTime))
        print("--------------------------")
        print(" There is a solution for the given game configuration")
        print("-----------Solution------------")
        solutionDepth = stack.size()
        memoryUsage = memoryUsage + getsizeof(stack)

        solutionString = ">"

        for z in range(0,solutionDepth):
            node = stack.pop()
            solutionString = solutionString + ")"
            x = node.toPoint.xordinate
            y = node.toPoint.yordinate
            toboard = str(PEGSOLITAIREBOARD[x][y])
            solutionString = solutionString + toboard[::-1]
            solutionString = solutionString + ","
            x = node.fromPoint.xordinate
            y = node.fromPoint.yordinate
            fromboard = str(PEGSOLITAIREBOARD[x][y])
            solutionString = solutionString + fromboard[::-1]
            solutionString = solutionString + "("
            solutionString = solutionString + ","

        solutionString = solutionString[:-1]
        solutionString = solutionString + "<"

        print(solutionString[::-1])

        print("------------------------")
        print(" Number of Nodes expanded: " + str(numberofNodes))
        print("------------------------")
        print(" Number of Moves made ( includes backtracking as well ) :" + str(numberofMoves))
        print("------------------------")
        print(" Memory consumed in Bytes: " + str(memoryUsage))

    else:
        executionTime = datetime.now() - startTime
        print("Execution time of the program: ", str(executionTime))
        print("There is no solution for the given board configuration")

        print("------------------------")
        print(" Number of Nodes expanded: " + str(numberofNodes))
        print("------------------------")
        print(" Number of Moves made ( includes backtracking as well ) :" + str(numberofMoves))
        print("------------------------")
        print(" Memory consumed in Bytes: " + str(memoryUsage))


    print("\n\n-----------Program Ended------------")














