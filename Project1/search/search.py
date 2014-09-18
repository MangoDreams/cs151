# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

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


def getListOfActions(current, parent):
     actions = []
     actions.append(current[1])
     while current in parent:
     	current = parent[current]
     	actions.insert(0, current[1])
     return actions
	

def depthFirstSearch0(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #initialize the search tree to DFS    
    fringe = util.Stack()
    visited = {}
    parent = {}   
    i = 0;
	
    if(problem.isGoalState(problem.getStartState())):
    	return []
    else:
    	for x in problem.getSuccessors(problem.getStartState()):
		parent[x[0]] = problem.getStartState()
		fringe.push(x)

    while not fringe.isEmpty():
    	expand = fringe.pop()
	if(problem.isGoalState(expand[0])):
		goalActions = getListOfActions(expand,parent)
		return goalActions
        
	visited[expand[0]] = 1
	for children in problem.getSuccessors(expand[0]):
		if children[0] in visited:
       			i += 1
		else:
			parent[children] = expand
			fringe.push(children)
   
    return []	

def depthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    visited = set()
   
    root = problem.getStartState()
    fringe.push(root)
    visited.add(root[0])
    i = 0

    while not fringe.isEmpty():
  	expand = fringe.pop()
	
	current_state = expand[0]
	action_list = expand[1]
	print current_state

	if(problem.isGoalState(current_state)):
		return action_list
	
	for child in problem.getSuccessors(expand):
		if(i < 1): 
			print child
		next_state = child[0][0]
		if not next_state in visited:
			visited.add(next_state)
			fringe.push(child[0])
	i += 1
   
    print "fail"
    return []

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    visited = set()
   
    root = problem.getStartState()
    fringe.push(root)
    visited.add(root[0])

    while not fringe.isEmpty():
  
  	expand = fringe.pop()
	
	current_state = expand[0]
	action_list = expand[1]
	print current_state

	if(problem.isGoalState(current_state)):
		return action_list
	
	for child in problem.getSuccessors(expand):
		next_state = child[0][0]
		if not next_state in visited:
			visited.add(next_state)
			fringe.push(child[0])
   
    print "fail"
    return []


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    visited = {}
    parent = {}   
    i = 0;
	
    if(problem.isGoalState(problem.getStartState())):
    	return []
    else:
    	for x in problem.getSuccessors(problem.getStartState()):
		parent[x[0]] = problem.getStartState()
		fringe.push(x, problem.getCostOfActions(getListOfActions(x,parent)))

    while not fringe.isEmpty():
    	expand = fringe.pop()
	if(problem.isGoalState(expand[0])):
		goalActions = getListOfActions(expand,parent)
		return goalActions
        
	visited[expand[0]] = 1
	for children in problem.getSuccessors(expand[0]):
		if children[0] in visited:
       			i += 1
		else:
			parent[children] = expand
			fringe.push(children, problem.getCostOfActions(getListOfActions(children,parent)))
   
    return []	

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
   
    fringe = util.PriorityQueue()
    visited = {}
    parent = {}   
    i = 0;
	
    if(problem.isGoalState(problem.getStartState())):
    	return []
    else:
    	for x in problem.getSuccessors(problem.getStartState()):
		parent[x[0]] = problem.getStartState()
		fringe.push(x, problem.getCostOfActions(getListOfActions(x,parent)) + heuristic(x[0],problem))

    while not fringe.isEmpty():
    	expand = fringe.pop()
	if(problem.isGoalState(expand[0])):
		goalActions = getListOfActions(expand,parent)
		return goalActions
        
	visited[expand[0]] = 1
	for children in problem.getSuccessors(expand[0]):
		if children[0] in visited:
       			i += 1
		else:
			parent[children] = expand
			fringe.push(children, problem.getCostOfActions(getListOfActions(children,parent)) + heuristic(children[0],problem))
   
    return []	

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
