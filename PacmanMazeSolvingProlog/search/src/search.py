# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
from spade import pyxf
from game import Directions

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def breadthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"

  #myXSB = pyxf.swipl("C:/Program Files (x86)/swipl/bin/swipl.exe")
  myXSB = pyxf.xsb("C:/workarea/XSB/bin/xsb.bat")
  myXSB.load("maze.P")
  myXSB.load("bfs.P")
  res = myXSB.query("doBFS(start,Direction).")

  dirList = res[0]['Direction']
  dirList = dirList.replace("[","")
  dirList = dirList.replace("]","")
  dirList = dirList.split(",")
  dList = []

  for dir in reversed(dirList):
      if dir == "south":
          dList.append(Directions.SOUTH)

      if dir == "north":
          dList.append(Directions.NORTH)

      if dir == "east":
          dList.append(Directions.EAST)

      if dir == "west":
          dList.append(Directions.WEST)

  return dList;



def depthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"

  # load the program
  myXsb = pyxf.xsb("C:/workarea/XSB/bin/xsb.bat")
  myXsb.load("maze.P")
  myXsb.load("dfs1.P")
  # the visited initial list is empty
  res = myXsb.query("dfs(start,[], Direction).")

  dirList = res[0]['Direction']

  dirList = dirList.replace("[","")
  dirList = dirList.replace("]","")
  dirList = dirList.split(",")
  dList = []

  i = 0;
  while i < (dirList.__len__() - 1):
      if dirList[i] == "south":
          dList.append(Directions.SOUTH)

      if dirList[i] == "north":
          dList.append(Directions.NORTH)

      if dirList[i] == "east":
          dList.append(Directions.EAST)

      if dirList[i] == "west":
          dList.append(Directions.WEST)

      i = i + 1;

  return dList;


def BreadthFirstSearchCorners(problem):
  """
  Search the deepest nodes in the search tree first [p 85].

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  resPaths = []
  #myXSB = pyxf.swipl("C:/Program Files (x86)/swipl/bin/swipl.exe")
  #----------------------------------------------------------
  myXSB = pyxf.xsb("C:/workarea/XSB/bin/xsb.bat")
  myXSB.load("maze.P")
  myXSB.load("bfs.P")

  res = myXSB.query("doBFS(start,Direction).")
  print(res)
  path1 = res[0]['Direction']
  resPaths.append(path1)

  #----------------------------------------------------------

  myXSB = pyxf.xsb("C:/workarea/XSB/bin/xsb.bat")
  myXSB.load("maze1.P")
  myXSB.load("bfs.P")

  res = myXSB.query("doBFS(start,Direction).")
  print(res)
  path2 = res[0]['Direction']
  resPaths.append(path2)

  #---------------------------------------------------------
  myXSB = pyxf.xsb("C:/workarea/XSB/bin/xsb.bat")
  myXSB.load("maze2.P")
  myXSB.load("bfs.P")

  res = myXSB.query("doBFS(start,Direction).")
  print(res)
  path3 = res[0]['Direction']
  resPaths.append(path3)
  #---------------------------------------------------------

  myXSB = pyxf.xsb("C:/workarea/XSB/bin/xsb.bat")
  myXSB.load("maze3.P")
  myXSB.load("bfs.P")
  res = myXSB.query("doBFS(start,Direction).")
  print(res)
  path4 = res[0]['Direction']
  resPaths.append(path4)

  dList = []
  for dirList in resPaths:
      dirList = dirList.replace("[","")
      dirList = dirList.replace("]","")
      dirList = dirList.split(",")
      for dir in reversed(dirList):
          if dir == "south":
              dList.append(Directions.SOUTH)

          if dir == "north":
              dList.append(Directions.NORTH)

          if dir == "east":
              dList.append(Directions.EAST)

          if dir == "west":
              dList.append(Directions.WEST)

  return dList;

      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  myXSB = pyxf.xsb("C:/workarea/XSB/bin/xsb.bat")
  myXSB.load("astarmaze.P")
  myXSB.load("astarHeuristic.P")
  myXSB.load("astar.P")
  res = myXSB.query("doAstar(start,Direction).")

  dirList = res[0]['Direction']
  dirList = dirList.replace("[","")
  dirList = dirList.replace("]","")
  dirList = dirList.split(",")
  dList = []

  for dir in reversed(dirList):
      if dir == "south":
          dList.append(Directions.SOUTH)

      if dir == "north":
          dList.append(Directions.NORTH)

      if dir == "east":
          dList.append(Directions.EAST)

      if dir == "west":
          dList.append(Directions.WEST)

  return dList;
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch