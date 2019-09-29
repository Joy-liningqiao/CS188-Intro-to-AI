# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        if "Stop" in legalMoves:
            legalMoves.remove("Stop")


        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # print(scores)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        from statistics import mean
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        gActions=[g.getDirection() for g in newGhostStates]
        # print(gActions)
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsules=successorGameState.getCapsules()

        "*** YOUR CODE HERE ***"
        getDist = lambda x1, x2, y1, y2: min(abs(x1-x2),abs(y1-y2))
        manhattan = lambda x1, x2, y1, y2: (abs(x1-x2)+abs(y1-y2))/2

        foodList=newFood.asList()
        ghostDistances = []
        ghostDistancesMan = []
        for i in newGhostStates:
            x2, y2=i.getPosition()
            x1, y1= newPos
            dist = getDist(x1, x2, y1, y2)
            distM = manhattan(x1, x2, y1, y2)
            ghostDistances.append(dist)
            ghostDistancesMan.append(distM)
        capsuleDist=[]
        for c in capsules:
            x2, y2=c
            x1, y1= newPos
            distM = manhattan(x1, x2, y1, y2)
            capsuleDist.append(distM)
        if len(capsuleDist) != 0:
            cMin=min(capsuleDist)

        x=min(ghostDistances)
        y=min(ghostDistancesMan)

        if len(foodList)==0:
            m=0
        else:
            m=-5*(len(foodList))
        if len(capsules)==0:
            c=0
        else:
            c=1/4*len(capsules)
        if sum(newScaredTimes) != 0:
            if (action != gActions[0]) and y<=2:
                return -20*y
            else:
                return m+c
        else:
            if y<=5:
                return m+y+c 
            else:
                return m+c


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        currentDepth = self.depth
        evalFunc=self.evaluationFunction

        def max_value(gameState, currentDepth):

            if gameState.isLose() or gameState.isWin() or currentDepth==0:
                return evalFunc(gameState)

            v = float("-inf")
            legalActs = gameState.getLegalActions(0)

            for move in legalActs:
                successorGameState = gameState.generateSuccessor(0, move)
                v=max(v, min_value(successorGameState, currentDepth, 1))

            return v

        def min_value(gameState, currentDepth, ghostNum):

            if gameState.isLose() or gameState.isWin() or currentDepth==0:
                return evalFunc(gameState)

            v = float("inf")
            legalActs=gameState.getLegalActions(ghostNum)

            for move in legalActs:
                successorState=gameState.generateSuccessor(ghostNum, move)

                if ghostNum==gameState.getNumAgents()-1:
                    v=min(v, max_value(successorState, currentDepth-1))
                else:
                    v=min(v, min_value(successorState, currentDepth, ghostNum+1))

            return v

        legalActs = gameState.getLegalActions(0)
        minValues = [(min_value(gameState.generateSuccessor(0, m), currentDepth, 1), m) for m in legalActs]
        maxVal=float("-inf")
        maxIndex=0
        for i in minValues:
            if i[0]>maxVal:
                maxVal=i[0]
                maxIndex=minValues.index(i)
        return minValues[maxIndex][1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        currentDepth = self.depth
        evalFunc=self.evaluationFunction
        alpha=float("-inf")
        beta=float("inf")

        def max_value(gameState, currentDepth, alpha, beta):

            if gameState.isLose() or gameState.isWin() or currentDepth==0:
                return evalFunc(gameState)

            v = float("-inf")

            legalActs = gameState.getLegalActions(0)
            for move in legalActs:
                successorGameState = gameState.generateSuccessor(0, move)
                v=max(v, min_value(successorGameState, currentDepth, 1, alpha, beta))
                if v > beta:
                    return v
                alpha=max(alpha, v)
            return v

        def min_value(gameState, currentDepth, ghostNum, alpha, beta):

            if gameState.isLose() or gameState.isWin() or currentDepth==0:
                return evalFunc(gameState)

            v = float("inf")

            legalActs=gameState.getLegalActions(ghostNum)
            for move in legalActs:
                successorState=gameState.generateSuccessor(ghostNum, move)
                if ghostNum==gameState.getNumAgents()-1:
                    v=min(v, max_value(successorState, currentDepth-1, alpha, beta))
                    if v < alpha:
                        return v
                else:
                    v=min(v, min_value(successorState, currentDepth, ghostNum+1, alpha, beta))
                if v < alpha:
                    return v
                beta=min(beta, v)
            return v

        legalActs = gameState.getLegalActions(0)
        action=legalActs[0]
        v = float("-inf")
        for m in legalActs:
            successorGameState=gameState.generateSuccessor(0,m)
            maxNodeVal=min_value(successorGameState, currentDepth,1,alpha,beta)
            if (maxNodeVal>v):
                v=maxNodeVal
                action=m
            if(maxNodeVal>beta):
                return action
            alpha=max(alpha,maxNodeVal)
            
        return action
        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        currentDepth = self.depth
        evalFunc=self.evaluationFunction

        def max_value(gameState, currentDepth):

            if gameState.isLose() or gameState.isWin() or currentDepth==0:
                return evalFunc(gameState)

            v = float("-inf")
            legalActs = gameState.getLegalActions(0)

            for move in legalActs:
                successorGameState = gameState.generateSuccessor(0, move)
                v=max(v, min_value(successorGameState, currentDepth, 1))

            return v

        def min_value(gameState, currentDepth, ghostNum):

            if gameState.isLose() or gameState.isWin() or currentDepth==0:
                return evalFunc(gameState)

            v = 0
            legalActs=gameState.getLegalActions(ghostNum)

            for move in legalActs:
                successorState=gameState.generateSuccessor(ghostNum, move)

                if ghostNum==gameState.getNumAgents()-1:
                    v=v+((1/len(legalActs))*(max_value(successorState, currentDepth-1)))
                else:
                    v=v+(1/len(legalActs))*(min_value(successorState, currentDepth, ghostNum+1))

            return v

        legalActs = gameState.getLegalActions(0)
        minValues = [(min_value(gameState.generateSuccessor(0, m), currentDepth, 1), m) for m in legalActs]
        maxVal=0
        maxIndex=0
        for i in minValues:
            if i[0]>maxVal:
                maxVal=i[0]
                maxIndex=minValues.index(i)
        return minValues[maxIndex][1]


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: If no ghost is scared, go towards states that reduce food or capsules remaning
    if ghost is scared, go towards the ghost 
    """
    "*** YOUR CODE HERE ***"
    from statistics import mean

    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foodRemListLen = 0
    if (len(food.asList()) > 0):
        foodRemListLen = len(food.asList())

    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [state.scaredTimer for state in ghostStates]
    capsules = currentGameState.getCapsules()
    capsuleLen=1

    getDist = lambda x1, y1, x2, y2:  min(abs(x1-x2), abs(y1-y2))
    manhattan = lambda x1, y1, x2, y2:  (abs(x1-x2)+abs(y1-y2))/2
    ghostDistances = []
    for i in ghostStates:
        x2, y2=i.getPosition()
        x1, y1= pos
        dist = manhattan(x1, y1, x2, y2)
        ghostDistances.append(dist)
    x=min(ghostDistances)

    y=[]
    if foodRemListLen==0:
        m=0
    else:
        m=-4*(foodRemListLen)
    if len(capsules)==0:
        c=0
    else:
        c=1/(len(capsules))

    gameScore=currentGameState.getScore()


    if sum(scaredTimes)==0:
        return gameScore-(m+x+c)
    else:
        return gameScore-(m+c-x)

# Abbreviation
better = betterEvaluationFunction
