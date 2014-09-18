# perceptron.py
# -------------
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


# Perceptron implementation
import util
PRINT = True

class PerceptronClassifier:
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "perceptron"
        self.max_iterations = max_iterations
        self.weights = {}
        for label in legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def setWeights(self, weights):
        assert len(weights) == len(self.legalLabels);
        self.weights = weights;

    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
	self.features = trainingData[0].keys() # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.

	score = util.Counter()
	for iteration in range(self.max_iterations):
		print "Starting iteration ", iteration, "..."
		for i in range(len(trainingData)):
			dataPoint = trainingData[i]
			actual_y = trainingLabels[i]
			for y in self.legalLabels:
				score[y] = self.weights[y]*dataPoint
			predicted_y = score.argMax()
			if(actual_y != predicted_y):
				self.weights[actual_y] += dataPoint
				self.weights[predicted_y] -= dataPoint
		
	   

    def classify(self, data):
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


    def findHighWeightFeatures(self, label):
        featuresWeights = []

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

        return featuresWeights
