# inference.py
# ------------
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


import itertools
import util
import random
import busters
import game

class InferenceModule:
    """
    An inference module tracks a belief distribution over a ghost's location.
    This is an abstract class, which you should not modify.
    """

    ############################################
    # Useful methods for all inference modules #
    ############################################

    def __init__(self, ghostAgent):
        "Sets the ghost agent for later access"
        self.ghostAgent = ghostAgent
        self.index = ghostAgent.index
        self.obs = [] # most recent observation position

    def getJailPosition(self):
        return (2 * self.ghostAgent.index - 1, 1)

    def getPositionDistribution(self, gameState):
        """
        Returns a distribution over successor positions of the ghost from the given gameState.

        You must first place the ghost in the gameState, using setGhostPosition below.
        """
        ghostPosition = gameState.getGhostPosition(self.index) # The position you set
        actionDist = self.ghostAgent.getDistribution(gameState)
        dist = util.Counter()
        for action, prob in actionDist.items():
            successorPosition = game.Actions.getSuccessor(ghostPosition, action)
            dist[successorPosition] = prob
        return dist

    def setGhostPosition(self, gameState, ghostPosition):
        """
        Sets the position of the ghost for this inference module to the specified
        position in the supplied gameState.

        Note that calling setGhostPosition does not change the position of the
        ghost in the GameState object used for tracking the true progression of
        the game.  The code in inference.py only ever receives a deep copy of the
        GameState object which is responsible for maintaining game state, not a
        reference to the original object.  Note also that the ghost distance
        observations are stored at the time the GameState object is created, so
        changing the position of the ghost will not affect the functioning of
        observeState.
        """
        conf = game.Configuration(ghostPosition, game.Directions.STOP)
        gameState.data.agentStates[self.index] = game.AgentState(conf, False)
        return gameState

    def observeState(self, gameState):
        "Collects the relevant noisy distance observation and pass it along."
        distances = gameState.getNoisyGhostDistances()
        if len(distances) >= self.index: # Check for missing observations
            obs = distances[self.index - 1]
            self.obs = obs
            self.observe(obs, gameState)

    def initialize(self, gameState):
        "Initializes beliefs to a uniform distribution over all positions."
        # The legal positions do not include the ghost prison cells in the bottom left.
        self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        self.initializeUniformly(gameState)

    ######################################
    # Methods that need to be overridden #
    ######################################

    def initializeUniformly(self, gameState):
        "Sets the belief state to a uniform prior belief over all positions."
        pass

    def observe(self, observation, gameState):
        "Updates beliefs based on the given distance observation and gameState."
        pass

    def elapseTime(self, gameState):
        "Updates beliefs for a time step elapsing from a gameState."
        pass

    def getBeliefDistribution(self):
        """
        Returns the agent's current belief state, a distribution over
        ghost locations conditioned on all evidence so far.
        """
        pass

class ExactInference(InferenceModule):
    """
    The exact dynamic inference module should use forward-algorithm
    updates to compute the exact belief function at each time step.
    """

    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        
	noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
	
	#B(trueDistance) = P(E = noisyDistance | trueDistance)*B'(trueDistance)
	
        allPossible = util.Counter()
	for p in self.legalPositions:
       		if noisyDistance == None:
			allPossible[p] = 0
		else:
			trueDistance = util.manhattanDistance(p, pacmanPosition)
			if emissionModel[trueDistance] > 0:
				allPossible[p] = emissionModel[trueDistance]*self.beliefs[p]
	
	if noisyDistance == None:
		allPossible[self.getJailPosition()] = 1
       
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
       
	#B'(X[t+1]) = (sum over all Xt) P(X[t+1] | X[t])*B(X[t]) 
	
	allPossible = util.Counter()
	for oldPos in self.legalPositions:
		newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))
		for newPos, prob in newPosDist.items():
			allPossible[newPos] += prob*self.beliefs[oldPos]
	
        allPossible.normalize()
        self.beliefs = allPossible

    def getBeliefDistribution(self):
        return self.beliefs

class ParticleFilter(InferenceModule):
    """
    A particle filter for approximately tracking a single ghost.

    Useful helper functions will include random.choice, which chooses
    an element from a list uniformly at random, and util.sample, which
    samples a key from a Counter by treating its values as probabilities.
    """


    def __init__(self, ghostAgent, numParticles=300):
        InferenceModule.__init__(self, ghostAgent);
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles


    def initializeUniformly(self, gameState):
	self.particle_positions = []
	numLegalPositions = len(self.legalPositions)	

	if numLegalPositions < self.numParticles:
		for i in range(numLegalPositions):
			for j in range(int(self.numParticles/numLegalPositions)):
				self.particle_positions.append(self.legalPositions[i])

	else:
		stepping = int(numLegalPositions/self.numParticles)
		for i in range(0, numLegalPositions, stepping):
			self.particle_positions.append(self.legalPositions[i])

    def observe(self, observation, gameState):

        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()

        "*** YOUR CODE HERE ***"

	weights = util.Counter()
	i = 0	
	
	if noisyDistance == None:
		self.particle_positions = []
		while i != self.numParticles:
			self.particle_positions.append(self.getJailPosition())
			i += 1
	else:
		for p in self.particle_positions:
			trueDistance = util.manhattanDistance(p, pacmanPosition)
			#maybe more than one particle per position
			weights[p] += emissionModel[trueDistance]
	
		if weights.totalCount()	!= 0:
			self.particle_positions = []
			while i != self.numParticles:
				self.particle_positions.append(util.sample(weights))
				i += 1
		else:
			self.initializeUniformly(gameState)

    def elapseTime(self, gameState):
	
	new = []
	for old_pos in self.particle_positions:
		new.append(util.sample(self.getPositionDistribution(self.setGhostPosition(gameState,old_pos))))
	self.particle_positions = new

    def getBeliefDistribution(self):
        """
          Return the agent's current belief state, a distribution over
          ghost locations conditioned on all evidence and time passage. This method
          essentially converts a list of particles into a belief distribution (a Counter object)
        """
        "*** YOUR CODE HERE ***"
     	beliefs = util.Counter()
	for p in self.particle_positions:
		beliefs[p] += 1
	
	beliefs.normalize()
	return beliefs	

class MarginalInference(InferenceModule):
    "A wrapper around the JointInference module that returns marginal beliefs about ghosts."

    def initializeUniformly(self, gameState):
        "Set the belief state to an initial, prior value."
        if self.index == 1: jointInference.initialize(gameState, self.legalPositions)
        jointInference.addGhostAgent(self.ghostAgent)

    def observeState(self, gameState):
        "Update beliefs based on the given distance observation and gameState."
        if self.index == 1: jointInference.observeState(gameState)

    def elapseTime(self, gameState):
        "Update beliefs for a time step elapsing from a gameState."
        if self.index == 1: jointInference.elapseTime(gameState)

    def getBeliefDistribution(self):
        "Returns the marginal belief over a particular ghost by summing out the others."
        jointDistribution = jointInference.getBeliefDistribution()
        dist = util.Counter()
        for t, prob in jointDistribution.items():
            dist[t[self.index - 1]] += prob
        return dist

class JointParticleFilter:
    "JointParticleFilter tracks a joint distribution over tuples of all ghost positions."

    def __init__(self, numParticles=600):
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles

    def initialize(self, gameState, legalPositions):
        "Stores information about the game, then initializes particles."
        self.numGhosts = gameState.getNumAgents() - 1
        self.ghostAgents = []
        self.legalPositions = legalPositions
        self.initializeParticles()

    def initializeParticles(self):
        """
        Initialize particles to be consistent with a uniform prior.  

        Each particle is a tuple of ghost positions. Use self.numParticles for
        the number of particles. You may find the python package 'itertools' helpful.  
        Specifically, you will need to think about permutations of legal ghost
        positions, with the additional understanding that ghosts may occupy the
        same space. Look at the 'product' function in itertools to get an
        implementation of the catesian product. Note: If you use
        itertools, keep in mind that permutations are not returned in a random order;
        you must shuffle the list of permutations in order to ensure even placement
        of particles across the board. Use self.legalPositions to obtain a list of
        positions a ghost may occupy.

          ** NOTE **
            the variable you store your particles in must be a list; a list is simply a collection
            of unweighted variables (positions in this case). Storing your particles as a Counter or
            dictionary (where there could be an associated weight with each position) is incorrect
            and will produce errors

        """
        "*** YOUR CODE HERE ***"
	self.particle_positions = []
	
	possiblePermutations = list(itertools.product(self.legalPositions,self.legalPositions,self.legalPositions))
	random.shuffle(possiblePermutations)
	numLegalPositions = len(possiblePermutations)	

	if numLegalPositions < self.numParticles:
		for i in range(numLegalPositions):
			for j in range(int(self.numParticles/numLegalPositions)):
				self.particle_positions.append(possiblePermutations[i])
	else:
		stepping = int(numLegalPositions/self.numParticles)
		for i in range(0, numLegalPositions, stepping):
			self.particle_positions.append(possiblePermutations[i])
	
    def addGhostAgent(self, agent):
        "Each ghost agent is registered separately and stored (in case they are different)."
        self.ghostAgents.append(agent)

    def getJailPosition(self, i):
        return (2 * i + 1, 1);

    def observeState(self, gameState):
        pacmanPosition = gameState.getPacmanPosition()
        noisyDistances = gameState.getNoisyGhostDistances()
        if len(noisyDistances) < self.numGhosts: return
        emissionModels = [busters.getObservationDistribution(dist) for dist in noisyDistances]

        "*** YOUR CODE HERE ***"
	weights = util.Counter()
	for i in range(len(self.particle_positions)):	
		temp = 1
		for ghost_idx in range(self.numGhosts):
			if noisyDistances[ghost_idx] == None:
				new_particle = self.getParticleWithGhostInJail(self.particle_positions[i],ghost_idx)
				self.particle_positions[i] = new_particle
		
			else:
				trueDistance = util.manhattanDistance(self.particle_positions[i][ghost_idx],pacmanPosition)
				model = emissionModels[ghost_idx] 	
				temp *= model[trueDistance]
		weights[self.particle_positions[i]] += temp
		
	i = 0
	if weights.totalCount() != 0:
		self.particle_positions = []
		while i != self.numParticles:
			self.particle_positions.append(util.sample(weights))
			i += 1
	else:
		self.initializeParticles()

	
    def getParticleWithGhostInJail(self, particle, ghostIndex):
        particle = list(particle)
        particle[ghostIndex] = self.getJailPosition(ghostIndex)
        return tuple(particle)

    def elapseTime(self, gameState):
        """
        Samples each particle's next state based on its current state and the gameState.

        To loop over the ghosts, use:

          for i in range(self.numGhosts):
            ...

        Then, assuming that "i" refers to the index of the
        ghost, to obtain the distributions over new positions for that
        single ghost, given the list (prevGhostPositions) of previous
        positions of ALL of the ghosts, use this line of code:

          newPosDist = getPositionDistributionForGhost(setGhostPositions(gameState, prevGhostPositions),
                                                       i, self.ghostAgents[i])

        **Note** that you may need to replace "prevGhostPositions" with the
        correct name of the variable that you have used to refer to the
        list of the previous positions of all of the ghosts, and you may
        need to replace "i" with the variable you have used to refer to
        the index of the ghost for which you are computing the new
        position distribution.

        As an implementation detail (with which you need not concern
        yourself), the line of code above for obtaining newPosDist makes
        use of two helper functions defined below in this file:

          1) setGhostPositions(gameState, ghostPositions)
              This method alters the gameState by placing the ghosts in the supplied positions.

          2) getPositionDistributionForGhost(gameState, ghostIndex, agent)
              This method uses the supplied ghost agent to determine what positions
              a ghost (ghostIndex) controlled by a particular agent (ghostAgent)
              will move to in the supplied gameState.  All ghosts
              must first be placed in the gameState using setGhostPositions above.

              The ghost agent you are meant to supply is self.ghostAgents[ghostIndex-1],
              but in this project all ghost agents are always the same.
        """
        newParticles = []
        for oldParticle in self.particles:
            newParticle = list(oldParticle) # A list of ghost positions

            # now loop through and update each entry in newParticle...

            "*** YOUR CODE HERE ***"

            "*** END YOUR CODE HERE ***"
            newParticles.append(tuple(newParticle))
        self.particles = newParticles

    def getBeliefDistribution(self):
     	beliefs = util.Counter()
	for p in self.particle_positions:
		beliefs[p] += 1
	
	beliefs.normalize()
	return beliefs	

# One JointInference module is shared globally across instances of MarginalInference
jointInference = JointParticleFilter()

def getPositionDistributionForGhost(gameState, ghostIndex, agent):
    """
    Returns the distribution over positions for a ghost, using the supplied gameState.
    """

    # index 0 is pacman, but the students think that index 0 is the first ghost.
    ghostPosition = gameState.getGhostPosition(ghostIndex+1)
    actionDist = agent.getDistribution(gameState)
    dist = util.Counter()
    for action, prob in actionDist.items():
        successorPosition = game.Actions.getSuccessor(ghostPosition, action)
        dist[successorPosition] = prob
    return dist

def setGhostPositions(gameState, ghostPositions):
    "Sets the position of all ghosts to the values in ghostPositionTuple."
    for index, pos in enumerate(ghostPositions):
        conf = game.Configuration(pos, game.Directions.STOP)
        gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
    return gameState

