__author__ = 'mahathi'

from array import *
from collections import namedtuple
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

# The elements that are pushed to the stack re of this form
GameStackElement = namedtuple("GameStackElement", "fromPoint toPoint")

# a peg in a board is a point
Point = namedtuple("Point", "xordinate yordinate")

# For tracking memory usage
memoryUsage = 0

#Number of nodes visited
numberofNodes = 0

#Number of moves made
numberofMoves = 0

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


stack = SolitaireStack()

# print the current configuration of the board
def printBoard(gameBoard):
    for x in range(0, 7):
        print(gameBoard[x])

#count the number of pegs in the board
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
def playPegSolitaire(gameBoard, numberofPegs, depth):
    global numberofNodes
    global stack
    global numberofMoves
    # check if this is a goal state
    if goalReached(gameBoard, numberofPegs):
        return 1 # we need not play if this is goal
    if stack.size() in range (0, depth):
        for i in range(0, 7):
             for j in range(0, 7):
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
                                        # Now we can make a move
                                        gameBoard[i_2][j_2] = 'X'
                                        gameBoard[i_1][j_1] = '0'
                                        gameBoard[i][j] = '0'
                                        numberofPegs = numberofPegs - 1
                                        # As we have made a move , we have generated a new node
                                        # add this to the stack
                                        currPoint  = Point(i,j)
                                        jumpedPoint = Point(i_2,j_2)
                                        m = GameStackElement(fromPoint = currPoint,toPoint = jumpedPoint )
                                        #printBoard(gameBoard)
                                        #print("-------------------")
                                        # push to stack
                                        stack.push(m)
                                        numberofNodes = numberofNodes + 1
                                        numberofMoves = numberofMoves + 1
                                        # for this move, play the game again with this board configuration
                                        if playPegSolitaire(gameBoard, numberofPegs, depth):
                                            return 1
                                        # if I am executing below, i have not found a goal yet
                                        # pop out the stack
                                        stack.pop()
                                        # Now lets get back to the parent configuration
                                        gameBoard[i_2][j_2] = '0'
                                        gameBoard[i_1][j_1] = 'X'
                                        gameBoard[i][j] = 'X'
                                        numberofPegs = numberofPegs + 1
                                        numberofMoves = numberofMoves + 1

                                    # for each direction play the game in a recursive way
                                    # for each node in board play the game

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

    print(" Starting to generate a solution . . .")
    startTime = datetime.now()

    foundSolution  = 0;
    for h in range(1,(numberofPegs + 1)):
        # Make a deep copy of the board to reuse at every level of iteration
        tempGameBoard = copy.deepcopy(gameBoard)
        memoryUsage = memoryUsage + getsizeof(tempGameBoard)
        if playPegSolitaire(tempGameBoard, numberofPegs, h):
            foundSolution = 1
            break

    executionTime = datetime.now() - startTime
    print("Execution time of the program: ", str(executionTime))
    print("--------------------------")

    if foundSolution:
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
        print("There is no solution for the given board configuration")
        print("------------------------")
        print(" Number of Nodes expanded: " + str(numberofNodes))
        print("------------------------")
        print(" Number of Moves made ( includes backtracking as well ) :" + str(numberofMoves))
        print("------------------------")
        print(" Memory consumed in Bytes: " + str(memoryUsage))


    print("-----------Program Ended------------")
















