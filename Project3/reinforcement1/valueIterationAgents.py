# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
	for k in range(self.iterations):
		current_values = self.values.copy() 
		for state in self.mdp.getStates():
			if not self.mdp.isTerminal(state):
				value_list = []
				for action in self.mdp.getPossibleActions(state):
					value_list.append(self.getQValue(state,action))
				current_values[state] = max(value_list)
		self.values = current_values


    def getValue(self, state):
        return self.values[state]


    def computeQValueFromValues(self, state, action):
	q = 0
	for next_state,transition in self.mdp.getTransitionStatesAndProbs(state,action):
		q += transition*(self.mdp.getReward(state,action,next_state) + self.discount*self.getValue(next_state))
	return q	


    def computeActionFromValues(self, state):
	
	actions = self.mdp.getPossibleActions(state)
	q_values = []
	for action in actions:
		q_values.append(self.computeQValueFromValues(state,action))

	if(q_values == []):
		optimal_action = None
	else:
		idx = q_values.index(max(q_values))	
		optimal_action = actions[idx]
	
	return optimal_action		

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
