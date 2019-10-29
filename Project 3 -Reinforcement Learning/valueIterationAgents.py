# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util
import random

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.maxQValue=0
        
        self.statePolicy=util.Counter()
        self.runValueIteration()
            
    def runValueIteration(self):
      i=self.iterations
      while i !=0:
        self.values_k=util.Counter()
        for state in self.mdp.getStates():
          stateQValueDict=util.Counter()
          for action in self.mdp.getPossibleActions(state):
            stateQValueDict[(state, action)]=self.getQValue(state, action)
            self.statePolicy[state]=stateQValueDict.argMax()[1]
          self.values_k[state]=stateQValueDict[stateQValueDict.argMax()]
        self.values=self.values_k
        i-=1
         


        # Write value iteration code here
      "*** YOUR CODE HERE ***"

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qValueList=[]
        nextStateAndProbsList=self.mdp.getTransitionStatesAndProbs(state, action)
        for nextState in nextStateAndProbsList:
          t=nextState[1]
          r=self.mdp.getReward(state, action, nextState[0])
          qValueCalc=t*(r+(self.discount*self.values[nextState[0]]))
          qValueList.append(qValueCalc)
        return sum(qValueList)
        
        

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if state == self.mdp.isTerminal(state):
          return None
        else:
          if self.statePolicy[state] !=0:
            return self.statePolicy[state]
          else:
            return "north"
        # util.raiseNotDefined()

    def getPolicy(self, state):
      # print(self.computeActionFromValues(state))
      return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)
        
    def getQValue(self, state, action):
      return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        
        self.maxQValue=0
        self.statePolicy=util.Counter()
        self.runValueIteration()

    def runValueIteration(self):
      "*** YOUR CODE HERE ***"
      states= self.mdp.getStates()
      for i in range(self.iterations):
        state = states[i % len(states)]
        if not self.mdp.isTerminal(state):
          stateQValueDict=util.Counter()
          for action in self.mdp.getPossibleActions(state):
            stateQValueDict[(state, action)]=self.getQValue(state, action)
            self.statePolicy[state]=stateQValueDict.argMax()[1]
          self.values[state]=stateQValueDict[stateQValueDict.argMax()]

      
class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
      "*** YOUR CODE HERE ***"

      #compute predecessors of each state
      self.predecessorDict=util.Counter()
      for state in self.mdp.getStates():
        for action in self.mdp.getPossibleActions(state):
          nextStates=[x[0] for x in self.mdp.getTransitionStatesAndProbs(state, action)]
          for nextState in nextStates:
            self.predecessorDict.setdefault(nextState, set()).add(state)
      
      #getting diff of each state and its max q-value
      self.pq=util.PriorityQueue()
      for state in self.mdp.getStates():
        stateQValueDict=util.Counter()
        if not self.mdp.isTerminal(state):
          for action in self.mdp.getPossibleActions(state):
            stateQValueDict[(state, action)]=self.getQValue(state, action)
            self.statePolicy[state]=stateQValueDict.argMax()[1]
          diff=abs(self.values[state]-stateQValueDict[stateQValueDict.argMax()])
      
      #push into queue with lowest diff as priority (min-heap)
          self.pq.push(state, -diff)
      #iter over predecessors and explore those states with highest diff
      for i in range(0, self.iterations):
        if self.pq.isEmpty():
          break
        state=self.pq.pop()
        stateQValueDict=util.Counter()
        if not self.mdp.isTerminal(state):
          for action in self.mdp.getPossibleActions(state):
            stateQValueDict[(state, action)]=self.getQValue(state, action)
          self.values[state]=stateQValueDict[stateQValueDict.argMax()]
        if self.predecessorDict[state] != 0:
          for pre in set(self.predecessorDict[state]):
            PreQValueDict=util.Counter()
            for action in self.mdp.getPossibleActions(pre):
              PreQValueDict[(pre, action)]=self.getQValue(pre, action)
              self.statePolicy[pre]=PreQValueDict.argMax()[1]
            diff=abs(self.values[pre]-PreQValueDict[PreQValueDict.argMax()])
      
        #push into queue if the diff is greater than noise tolerated          
            if diff > self.theta:
              self.pq.update(pre, -diff)
