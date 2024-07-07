# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    from util import Stack
    state = Stack()
    visited=set()
    nowstate=problem.getStartState()
    visited.add(nowstate)
    dir=[]
    depth=0
    while not problem.isGoalState(nowstate):
        statelist=problem.getSuccessors(nowstate)
        for i in statelist:
            if visited.__contains__(i[0]):
                continue
            state.push((i[0],i[1],depth+1))
        step=state.pop()
        nowstate=step[0]
        visited.add(nowstate)
        depth=step[2]
        if len(dir) >= step[2]:
            dir = dir[:step[2]-1]
        dir.append(step[1])
    return dir
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    from util import Queue
    state=Queue()
    visited=set()
    nowstate=problem.getStartState()
    visited.add(nowstate)
    dir=[]
    state.push((nowstate,dir,0))
    step=state.pop()
    while (not problem.isGoalState(nowstate)):
        statelist=problem.getSuccessors(nowstate)
        for i in statelist:
            if visited.__contains__(i[0]):
                continue
            next_dir = step[1][:]
            next_dir.append(i[1])
            state.push((i[0],next_dir,i[2]))
            visited.add(i[0])
        if state.isEmpty():
            util.raiseNotDefined()
        step=state.pop()
        nowstate=step[0]
    return step[1]        
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    from util import PriorityQueue
    state=PriorityQueue()
    visited=set()
    nowstate=problem.getStartState()
    visited.add(nowstate)
    dir=[]
    priority=0
    dict={}
    state.push(nowstate,priority)
    dict[nowstate]=(dir,priority)
    step=state.pop()
    while (not problem.isGoalState(nowstate)):
        statelist=problem.getSuccessors(nowstate)
        for i in statelist:
            if visited.__contains__(i[0]):
                continue
            next_dir = dict[step][0][:]
            next_dir.append(i[1])
            state.update(i[0],priority+i[2])
            if(dict.__contains__(i[0]) and dict[i[0]][1]<priority+i[2]):
                continue
            dict[i[0]]=(next_dir,priority+i[2])
        if state.isEmpty():
            util.raiseNotDefined()
        step=state.pop()
        visited.add(step)
        nowstate=step
        priority=dict[step][1]
    return dict[step][0]        
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    from util import PriorityQueue
    state=PriorityQueue()
    visited=set()
    nowstate=problem.getStartState()
    visited.add(nowstate)
    dir=[]
    priority=0
    dict={}
    state.push(nowstate,priority+heuristic(nowstate,problem))
    dict[nowstate]=(dir,priority)
    step=state.pop()
    while (not problem.isGoalState(nowstate)):
        statelist=problem.getSuccessors(nowstate)
        for i in statelist:
            if visited.__contains__(i[0]):
                continue
            if(dict.__contains__(i[0]) and dict[i[0]][1]<priority+i[2]):
                continue
            next_dir = dict[step][0][:]
            next_dir.append(i[1])
            state.update(i[0],priority+i[2]+heuristic(i[0],problem))
            dict[i[0]]=(next_dir,priority+i[2])
        if state.isEmpty():
            util.raiseNotDefined()
        step=state.pop()
        visited.add(step)
        nowstate=step
        priority=dict[step][1]
    return dict[step][0]
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
