# naiveBayes.py
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


import util
import classificationMethod
import math


class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 1 # this is the smoothing parameter, ** use it in your train method **
        self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **

    def setSmoothing(self, k):
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):

        # might be useful in your code later...
        # this is a list of all features in the training set.
        self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));

        if (self.automaticTuning):
            kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
        else:
            kgrid = [self.k]

        self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
	count = util.Counter()
	self.P = util.Counter()
	self.P_conditional_zero = util.Counter()
	self.P_conditional_one = util.Counter()
	n = util.Counter()

	#P(y) = c(y)/n
	n_total = float(len(trainingLabels))
	for y in self.legalLabels:
			n[y] = float(trainingLabels.count(y))
			self.P[y] = n[y]/n_total
	
	
	# get counts, pixel can be zero or one
	for i in range(len(trainingLabels)):
		y = trainingLabels[i]
		dataPoint = trainingData[i]
		for f in self.features:		
			if (dataPoint[f] == 1):
				count[(y,f,1)] += 1
			else:
				count[(y,f,0)] += 1
		
	matches = []
	for k in kgrid:
		for y in self.legalLabels:
			for f in self.features:
				self.P_conditional_one[(y,f)] = (count[(y,f,1)] + k)/(n[y] + 2*k)
				self.P_conditional_zero[(y,f)] = (count[(y,f,0)] + k)/(n[y] + 2*k)
		
		j = 0
		for i in range(len(validationLabels)):
			actual_y = validationLabels[i]	
			dataPoint = validationData[i]
			predicted_y = self.calculateLogJointProbabilities(dataPoint).argMax()	
			if(predicted_y == actual_y):
				j += 1	
		
		matches.append(j)
	
	idx = matches.index(max(matches))
	self.k = kgrid[idx]
	
	for y in self.legalLabels:
		for f in self.features:
			self.P_conditional_one[(y,f)] = (count[(y,f,1)] + self.k)/(n[y] + 2*self.k)
			self.P_conditional_zero[(y,f)] = (count[(y,f,0)] + self.k)/(n[y] + 2*self.k)
	

    def classify(self, testData):
        guesses = []
        self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        
	return guesses

    def calculateLogJointProbabilities(self, datum):
        logJoint = util.Counter()

        "*** YOUR CODE HERE ***"
       	for y in self.legalLabels:
		logJoint[y] = math.log(self.P[y])
		for f in self.features:
			if(datum[f] == 1):
				logJoint[y] +=  math.log(self.P_conditional_one[(y,f)])
		
			else:
				logJoint[y] += math.log(self.P_conditional_zero[(y,f)])
        
	return logJoint

    def findHighOddsFeatures(self, label1, label2):
        featuresOdds = []

        "*** YOUR CODE HERE ***"
       	for f in self.features:
		numerator = self.P_conditional_one[(label1,f)]
		denominator = self.P_conditional_one[(label2,f)]
		featuresOdds.append(numerator/denominator)
	featuresOdds.sort()
	featuresOdds.reverse()
        return featuresOdds[:100]
