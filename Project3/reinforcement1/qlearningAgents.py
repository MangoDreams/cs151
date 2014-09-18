# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
	self.q = util.Counter()	

    def getQValue(self, state, action):
        "*** YOUR CODE HERE ***"
	#Counter already initialized to zero
	return self.q[(state,action)]

    def computeValueFromQValues(self, state):
	actions = self.getLegalActions(state)
	q_values = []
	for action in actions:
		q_values.append(self.getQValue(state,action))

	if(q_values == []):
		return 0.0
	else:
		return max(q_values)

    def computeActionFromQValues(self, state):
	actions = self.getLegalActions(state)
	q_values = []
	for action in actions:
		q_values.append(self.getQValue(state,action))

	if(q_values == []):
		optimal_action = None
	else:
		optimal_idx = []
		new_max = 0.0
		old_max = 0.0
		temp = q_values
			
		while(new_max == old_max):
			old_max = new_max
			old_max = max(temp)
			idx = temp.index(old_max)
			optimal_idx.append(idx)
			q_values.pop(idx)
			if (temp == []):
				break;
			else:
				new_max = max(temp)
					
		idx = random.choice(optimal_idx)	
		optimal_action = actions[idx]
	
	return optimal_action		

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
	if not(legalActions == []):
		if(util.flipCoin(self.epsilon)):
			action = random.choice(legalActions)
		else:
			action = self.getPolicy(state)
	
        return action

    def update(self, state, action, nextState, reward):
	sample = reward + self.discount*self.getValue(nextState)
	self.q[(state,action)] = (1-self.alpha)*self.getQValue(state,action) + self.alpha*(sample) 	       	

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)
        
    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
	sum = 0.0
        features = self.featExtractor.getFeatures(state,action)
	for feature in features.keys():
		sum += features[feature]*self.weights[feature]
	
	return sum


    def update(self, state, action, nextState, reward):
	
	difference = (reward + self.discount*self.getValue(nextState)) - self.getQValue(state,action)
	features = self.featExtractor.getFeatures(state,action)
	for feature in features.keys():
		self.weights[feature] = self.weights[feature] + self.alpha*difference*features[feature]	

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
