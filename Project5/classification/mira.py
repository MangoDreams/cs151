# mira.py
# -------
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


# Mira implementation
import util
PRINT = True

def dotProduct(u,v):
	value = 0.0
	for f in u:	
		u[f] *= v[f]
		value += u[f]
	return value

class MiraClassifier:

    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        
	
	old_weights = self.weights
	for c in Cgrid:
		matches = []
		weights = []
		self.weights = old_weights
		score = util.Counter()
		for iteration in range(self.max_iterations):
			for i in range(len(trainingData)):
				dataPoint = trainingData[i]
				actual_y = trainingLabels[i]
				for y in self.legalLabels:
					score[y] = self.weights[y]*dataPoint
				predicted_y = score.argMax()
				if(actual_y != predicted_y):
					dp = 2*dotProduct(dataPoint,dataPoint)
					tau = min(c,(((self.weights[predicted_y]-self.weights[actual_y])*dataPoint + 1.0)/dp))
					for f in dataPoint:
						dataPoint[f] *= tau
					self.weights[actual_y] += dataPoint
					self.weights[predicted_y] -= dataPoint
					
		j = 0
		predicted = self.classify(validationData)
		for i in range(len(validationLabels)):
			actual_y = validationLabels[i]	
			predicted_y = predicted[i]
			if(predicted_y == actual_y):
				j += 1	
		matches.append(j)
		weights.append(self.weights)
		
	idx = matches.index(max(matches))
	self.weights = weights[idx]

    def classify(self, data ):
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


    def findHighOddsFeatures(self, label1, label2):
        featuresOdds = []

        "*** YOUR CODE HERE ***"

        return featuresOdds
