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

### BEGIN: HELPER FUNCTIONS NOT PROVIDED IN STARTER CODE ###

#user-defined class to make passing things nicer.
class Node:
	
	def __init__(self,state,depth,agent_idx = 0, alpha = 0, beta = 0):
		self.state = state
		self.depth = depth
		self.idx = agent_idx
		self.alpha = alpha
		self.beta = beta

	def isTerminal(self):
		return (self.state.isWin() or self.state.isLose() or self.depth == 0)
	
	def getIdx(self):
		return self.idx
	
	def getState(self):
		return self.state
	
	def getDepth(self):
		return self.depth
	
	def getAlpha(self):
		return self.alpha
	
	def getBeta(self):
		return self.beta

def listDistances(state,list):

	distances = []	
	for item in list: 
		distance = abs(state[0] - item[0]) + abs(state[1] - item[1])
		distances.append(distance)
	
	distances.sort()	
	return distances

### END: HELPER FUNCTIONS NOT PROVIDED IN STARTED CODE ###



class ReflexAgent(Agent):

    def getAction(self, gameState):
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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
	#initialize a float score that we will add to later
	score = 0.0 	

	#food
	food_positions = newFood.asList()
	
	#get positions of Ghosts
	ghost_positions = []
	for ghost in newGhostStates:
		ghost_positions.append(ghost.getPosition())

	#get sorted distances 
	food_distances = listDistances(newPos,food_positions) 
	ghost_distances = listDistances(newPos,ghost_positions)

	#discourage waiting		
	if(action == 'Stop'):
		score -= 5
	
	#there is distance to food ==> BAD
	if(food_distances != []):
		score  -= food_distances[0]
	
	#there is distance to ghost ==> GOOD
	if(ghost_distances != []):
		score += ghost_distances[0]

	#More food => GOOD
	if(currentGameState.getNumFood() > successorGameState.getNumFood()):
		score += 25
	
	#ghost about to eat PACMAN => BAD
	if(ghost_distances[0] == 0):
		score -= 75.0
	
	return score

def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        "*** YOUR CODE HERE ***"
        # Implemented PseudoCode from Lecture 6
	 
	minmax_map = {}
	depth = self.depth	
	
	for action in gameState.getLegalActions():
		#generate next states for PACMAN
		successor_node = Node(gameState.generateSuccessor(0,action),depth,1)
		#pacman's successors are minimizers
		v = self.minValue(successor_node) 
		minmax_map[v] = action
	
	v_max = max(minmax_map.keys())
	optimal_action = minmax_map[v_max]		
	
	return optimal_action
	
    def maxValue(self,max_node):

	state = max_node.getState()
	depth = max_node.getDepth()
	if(max_node.isTerminal()):
		return self.evaluationFunction(state)	

	else:
		#initialize v to a large negative value
		v = -100000000.0 
		for action in state.getLegalActions(0):
			successor_node = Node(state.generateSuccessor(0,action),depth,1)
			v = max(v,self.minValue(successor_node))
		return v

    def minValue(self,min_node):

	state = min_node.getState()
	idx = min_node.getIdx()
	depth = min_node.getDepth()

	if(min_node.isTerminal()):
		return self.evaluationFunction(state)	

	else:
	#initialize v to a large postive value
		v = 1000000000.0
		if (idx == state.getNumAgents()- 1):
			for action in state.getLegalActions(idx):
				successor_node = Node(state.generateSuccessor(idx,action),depth-1)
				v = min(v,self.maxValue(successor_node))
		else:
			for action in state.getLegalActions(idx):
				successor_node = Node(state.generateSuccessor(idx,action),depth,idx+1)
				v = min(v,self.minValue(successor_node))
		return v


class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        #Modified minmax with a few changes

	alpha_beta_map = {}
	depth = self.depth	

	#alpha upper bound and beta lower bound	
	alpha = -1000000000.0
	beta = 1000000000.0
	
	for action in gameState.getLegalActions():
		#generate next states for PACMAN
		successor_node = Node(gameState.generateSuccessor(0,action),depth,1,alpha,beta)
		#pacman's successors are minimizers
		v = self.minValue(successor_node) 
		alpha_beta_map[v] = action
		alpha = max(alpha,v)
	
	v_max = max(alpha_beta_map.keys())
	optimal_action = alpha_beta_map[v_max]		
	
	return optimal_action
	
    def maxValue(self,max_node):

	state = max_node.getState()
	depth = max_node.getDepth()
	alpha = max_node.getAlpha()
	beta = max_node.getBeta()

	if(max_node.isTerminal()):
		return self.evaluationFunction(state)	

	else:
		#initialize v to a large negative value
		v = -100000000.0 
		for action in state.getLegalActions(0):
			successor_node = Node(state.generateSuccessor(0,action),depth,1,alpha,beta)
			v = max(v,self.minValue(successor_node))
			if (v > beta):
				return v
			alpha = max(alpha,v)
		return v

    def minValue(self,min_node):

	state = min_node.getState()
	idx = min_node.getIdx()
	depth = min_node.getDepth()
	alpha = min_node.getAlpha()
	beta = min_node.getBeta()

	if(min_node.isTerminal()):
		return self.evaluationFunction(state)	

	else:
	#initialize v to a large postive value
		v = 1000000000
		if (idx == state.getNumAgents()- 1):
			for action in state.getLegalActions(idx):
				successor_node = Node(state.generateSuccessor(idx,action),depth-1,0,alpha,beta)
				v = min(v,self.maxValue(successor_node))
				if (v < alpha):
					return v
				beta = min(beta,v)
		else:
			for action in state.getLegalActions(idx):
				successor_node = Node(state.generateSuccessor(idx,action),depth,idx+1,alpha,beta)
				v = min(v,self.minValue(successor_node))
				if (v < alpha):
					return v
				beta = min(beta,v)
		return v

class ExpectimaxAgent(MultiAgentSearchAgent):

        # Implemented PseudoCode from Lecture 6
	 
    def getAction(self, gameState):
	expectimax_map = {}
	depth = self.depth	
	
	for action in gameState.getLegalActions():
		#generate next states for PACMAN
		successor_node = Node(gameState.generateSuccessor(0,action),depth,1)
		#pacman's successors are minimizers
		v = self.expectedValue(successor_node) 
		expectimax_map[v] = action
	
	v_max = max(expectimax_map.keys())
	optimal_action = expectimax_map[v_max]		
	
	return optimal_action

    def maxValue(self,max_node):

	state = max_node.getState()
	depth = max_node.getDepth()
	if(max_node.isTerminal()):
		return self.evaluationFunction(state)	

	else:
		#initialize v to a large negative value
		v = -100000000.0 
		for action in state.getLegalActions(0):
			successor_node = Node(state.generateSuccessor(0,action),depth,1)
			v = max(v,self.expectedValue(successor_node))
		return v

    def expectedValue(self,chance_node):

	state = chance_node.getState()
	idx = chance_node.getIdx()
	depth = chance_node.getDepth()

	if(chance_node.isTerminal()):
		return self.evaluationFunction(state)	

	else:
		#running sum across neighboring states
		v = 0.0
		if (idx == state.getNumAgents()- 1):
			for action in state.getLegalActions(idx):
				successor_node = Node(state.generateSuccessor(idx,action),depth-1)
				v += self.maxValue(successor_node)
		else:
			for action in state.getLegalActions(idx):
				successor_node = Node(state.generateSuccessor(idx,action),depth,idx+1)
				v += self.expectedValue(successor_node)
	
		#average = sum/n 	
		return v/len(state.getLegalActions(idx))

def betterEvaluationFunction(currentGameState):

	#useful things to know
        GhostStates = currentGameState.getGhostStates()
        food = currentGameState.getFood()
	newScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
	currPos = currentGameState.getPacmanPosition()
	
	#initialize a float score that we will add to later
	score = scoreEvaluationFunction(currentGameState) 	

	#food
	food_positions = food.asList()
	
	#get positions of Ghosts
	ghost_positions = []
	for ghost in GhostStates:
		ghost_positions.append(ghost.getPosition())

	#get sorted distances 
	food_distances = listDistances(currPos,food_positions) 
	ghost_distances = listDistances(currPos,ghost_positions)

	#ghost about to eat PACMAN => BAD
	if(ghost_distances[0] == 0):
		score -= 100.0
	
	#there is distance to food ==> BAD
	while(food_distances != []):
		score  -= food_distances.pop()
	
	#there is distance to ghost ==> GOOD
	if(ghost_distances != []):
		score += ghost_distances.pop()
	
	return score
	
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

