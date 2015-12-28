# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)

        #print(successorGameState)
        #print("---------")
        newPos = successorGameState.getPacmanPosition()
        #print(newPos)
        newFood = successorGameState.getFood()
        #print(newFood)
        newGhostStates = successorGameState.getGhostStates()
        #print(newGhostStates)
        #print("---------")
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # for a given game state, calculate the distance of the current position of pacman to  the nearest food
        foodArray = newFood.asList()
        distancesToFood = []
        sumOfDistancesToFood = 0

        for food in foodArray:
            distanceToFood =  manhattanDistance(newPos,food)
            distancesToFood.append(distanceToFood)
            sumOfDistancesToFood = sumOfDistancesToFood + distanceToFood

        # if in the next position, there is no food left, we will emerge victorious
        if sumOfDistancesToFood == 0:
            nearestDistance = 0
        else: # calculate this minimum distance.
            nearestDistance = min(distancesToFood)

        # Always choose a path such that distances between the pacman and ghosts is maximum
        sumOfDistancesToGhost = 0

        for ghost in newGhostStates:
            sumOfDistancesToGhost = sumOfDistancesToGhost + manhattanDistance(newPos, ghost.getPosition())

        # take a weighted average between distance to ghosts and food. Avoiding ghosts is higher priority

        return sumOfDistancesToGhost * 0.3 + ((1/(nearestDistance +1)) * 0.6) #( the + 1 is to avoid division by zero error)


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

nodesExploredMiniMax = 0
class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        "*** YOUR CODE HERE ***"
        # Choose one of the best actions
        #for a game state expand the moves upto depth d, and apply minimax algorithm
        maxDepth = self.depth
        global nodesExploredMiniMax
        ghostMoves = 10
        pacmanMoves = 20
        legalMoves = gameState.getLegalActions(0) # get all possible moves for the pacman agent
        scores = [self.runMiniMaxAlg(self,gameState.generatePacmanSuccessor(action), self.depth,ghostMoves, 1) for action in legalMoves]
        # for each of the move, select the max score
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        #print nodes explored
        print("nodes explored :")
        print(nodesExploredMiniMax)
        return legalMoves[chosenIndex]

    def runMiniMaxAlg(self, minimaxAgent, gameState, maxDepth,moving, ghostAgentIndex):

        global nodesExploredMiniMax
        nodesExploredMiniMax = nodesExploredMiniMax + 1
        # these are the terminal nodes for which the evaluation function evaluates and gives a value to the board
        if gameState.isWin() or gameState.isLose() or maxDepth == 0:
            return (self.evaluationFunction(gameState))

        if moving == 10:
            #the ghost's moves
            ghostStates = gameState.getGhostStates()
            minScore = float("inf")
            if ghostAgentIndex == len(ghostStates): # this is the last ghost, we have now generated all the ghost moves, now check with pacman
                legalMoves = gameState.getLegalActions(ghostAgentIndex) # get all possible moves for the ghost agent
                # for all paths, play with pacman now
                scores = [self.runMiniMaxAlg(self,gameState.generateSuccessor(ghostAgentIndex, action), maxDepth - 1,20, ghostAgentIndex) for action in legalMoves]
                minScore = min(scores)
                return minScore
            else:
                legalMoves = gameState.getLegalActions(ghostAgentIndex)
                scores = [self.runMiniMaxAlg(self,gameState.generateSuccessor(ghostAgentIndex, action), maxDepth,10, ghostAgentIndex + 1) for action in legalMoves]
                minScore = min(scores)
                return minScore

            return minScore

        if moving == 20:
            #pacman moves
            maxScore = float("-inf")
            legalMoves = gameState.getLegalActions(0) # get actions of the pacman
            # for all possible moves of pacman run the algorithm to determine the maximum score path
            scores = [self.runMiniMaxAlg(self,gameState.generatePacmanSuccessor(action), maxDepth - 1,10, 1) for action in legalMoves]
            maxScore = max(scores)
            return maxScore

        # while evaluating the min states, we take the ghost moves into consideration



nodesExpanded = 0
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)

    """

    def getAction(self, gameState):
        global nodesExpanded
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        "*** YOUR CODE HERE ***"
        # The look ahead depth of the game
        maxDepth = self.depth
        #during the minimax process, the player who moves is denoted by following values
        ghostMoves = 10
        pacmanMoves = 20
        # the alpha and beta values are initialized
        alpha = float("-inf")
        beta = float("+inf")
        legalMoves = gameState.getLegalActions(0)
        nodesExpanded = nodesExpanded + 1
        scores = [self.runAlphaBetaAlg(self,gameState.generatePacmanSuccessor(action), self.depth,ghostMoves, 1, alpha, beta) for action in legalMoves]
        # for each of the move, select the max score
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        print("nodes expanded")
        print(nodesExpanded)
        return legalMoves[chosenIndex]


    def runAlphaBetaAlg(self, minimaxAgent, gameState, maxDepth,moving, ghostAgentIndex, alpha, beta):
        # these are the terminal nodes for which the evaluation function evaluates and gives a value to the board
        global nodesExpanded
        #print(gameState)
        #print("---------")
        if gameState.isWin() or gameState.isLose() or maxDepth == 0:
            return (self.evaluationFunction(gameState))


        if moving == 10:
            #the ghost's moves
            score = float("inf")
            if ghostAgentIndex == len(gameState.getGhostStates()): # this is the last ghost, we have now generated all the ghost moves, now check with pacman
                legalMoves = gameState.getLegalActions(ghostAgentIndex) # get all possible moves for the ghost agent
                for action in legalMoves:
                    nodesExpanded = nodesExpanded + 1
                    score = self.runAlphaBetaAlg(self,gameState.generateSuccessor(ghostAgentIndex, action), maxDepth - 1,20, ghostAgentIndex, alpha, beta)
                    if score < alpha:
                        return score # this is the final value of the node, return without exploring other actions( pruning)
                    if score < beta: # update the new beta value, the further runs of this algorithm runs with this new beta value
                        beta = score

            else:
                legalMoves = gameState.getLegalActions(ghostAgentIndex)
                for action in legalMoves:
                    nodesExpanded = nodesExpanded + 1
                    score = self.runAlphaBetaAlg(self,gameState.generateSuccessor(ghostAgentIndex, action), maxDepth,10, ghostAgentIndex + 1, alpha, beta)
                    if score < alpha: # we are pruning. no need to check other moves, as we have got less than alpha
                        return score
                    if score < beta:  # update the new beta value, the further runs of this algorithm runs with this new beta value
                        beta = score

            return score

        if moving == 20:
            #pacman moves
            score = float("-inf")
            legalMoves = gameState.getLegalActions(0) # get actions of the pacman
            for action in legalMoves:
                nodesExpanded = nodesExpanded + 1
                score = self.runAlphaBetaAlg(self,gameState.generatePacmanSuccessor(action), maxDepth - 1,10, 1, alpha, beta)
                if score > beta:# we are pruning. no need to check other moves, as we have got greater than beta
                    return score
                if(score > alpha): # update the new alpha value, this is the maximum of the previous maximums we obtained
                    alpha = score
            return score


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

