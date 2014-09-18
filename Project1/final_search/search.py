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

class Node:
	
	def __init__(self,state,actions,new_action):
	
		self.state = state
		
		self.path_to_state = actions[:]
		
		if new_action != 'Start':
			self.path_to_state.append(new_action)

	def getState(self):
		return self.state

	def returnPath(self):
		return self.path_to_state


def getListOfActions(current, parent):
     actions = []
     actions.append(current[1])
     while current in parent:
     	current = parent[current]
     	actions.insert(0, current[1])
     return actions
    

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
	
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

def breadthFirstSearch(problem):
	
	#returns path to final state using BFS
	fringe = util.Queue()
	visited = set()
	begin = problem.getStartState()

	root = Node(begin,[],'Start')
	fringe.push(root)
	visited.add(begin)
	
	while not fringe.isEmpty():

		expand = fringe.pop()
		path = expand.returnPath()
		state = expand.getState()
		
		if(problem.isGoalState(state)):
			return path 
		
		for successors in problem.getSuccessors(state):
				if not successors[0] in visited:
					visited.add(successors[0])
					child = Node(successors[0],path,successors[1])
					fringe.push(child)

	print "Failure"
	return root.returnPath() 

def uniformCostSearch(problem):
	#returns path to final state using UCS
	fringe = util.PriorityQueue()
	visited = set()
	cost_map = {}
	begin = problem.getStartState()

	root = Node(begin,[],'Start')
	fringe.push(root,problem.getCostOfActions(root.returnPath()))
	visited.add(begin)
	
	while not fringe.isEmpty():

		expand = fringe.pop()
		path = expand.returnPath()
		state = expand.getState()
		
		if(problem.isGoalState(state)):
			return path
		
		for successors in (problem.getSuccessors(state)):
			child = Node(successors[0],path,successors[1])
			if not successors[0] in visited:
					visited.add(successors[0])
					fringe.push(child,problem.getCostOfActions(child.returnPath()))
					cost_map[child.getState()] = problem.getCostOfActions(child.returnPath())

			if child.getState() in cost_map:
				if (cost_map[child.getState()] >  problem.getCostOfActions(child.returnPath())):
						fringe.push(child,problem.getCostOfActions(child.returnPath()))
	
	print "Failure"
	return root.returnPath() 



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):

	#returns path to final state using UCS
	fringe = util.PriorityQueue()
	visited = set()
	cost_map = {}
	begin = problem.getStartState()

	root = Node(begin,[],'Start')
	fringe.push(root,problem.getCostOfActions(root.returnPath()) + heuristic(root.getState(),problem))
	visited.add(begin)
	
	while not fringe.isEmpty():

		expand = fringe.pop()
		path = expand.returnPath()
		state = expand.getState()
		
		if(problem.isGoalState(state)):
			return path
		
		for successors in (problem.getSuccessors(state)):
			child = Node(successors[0],path,successors[1])
			if not successors[0] in visited:
					visited.add(successors[0])
					fringe.push(child,problem.getCostOfActions(child.returnPath()) + heuristic(child.getState(),problem))
					cost_map[child.getState()] = problem.getCostOfActions(child.returnPath()) + heuristic(child.getState(),problem)
			if child.getState() in cost_map:
				if (cost_map[child.getState()] >  problem.getCostOfActions(child.returnPath()) +  heuristic(child.getState(),problem)):
						fringe.push(child,problem.getCostOfActions(child.returnPath()) + heuristic(child.getState(),problem))
	
	print "Failure"
	return root.returnPath() 
	

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
