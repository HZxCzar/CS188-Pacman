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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print(newPos)
        # print(newFood)
        # print(newGhostStates)
        # print(newScaredTimes)
        DisWithGhost= 0
        DisMini=99999
        DisWithFood = 0
        DisWithFoodMini=99999
        FoodCount=0
        for i in newFood.asList():
            DisWithFood=max(DisWithFood,manhattanDistance(newPos, i))
            FoodCount+=manhattanDistance(newPos, i)
            if manhattanDistance(newPos, i)<=1:
                continue
            DisWithFoodMini=min(DisWithFoodMini,manhattanDistance(newPos, i))
        for i in newGhostStates:
            DisWithGhost += manhattanDistance(newPos, i.getPosition())
            DisMini=min(DisMini,manhattanDistance(newPos, i.getPosition()))
        if DisMini<=1:
                print("danger")
                return -1000
        if DisMini>=3:
            print(DisWithFoodMini)
            print(1/DisWithFood)
            successorGameState.data.score=100/DisWithFood-10/DisWithGhost+random.randint(0,1)
            return successorGameState.getScore()
        successorGameState.data.score=1000/DisWithFood-1/DisWithGhost
        print(successorGameState.data.score)
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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
    # def minimax(self,gameState: GameState,index):
    #     if (self.depth<=0 and index==0) or gameState.isWin() or gameState.isLose():
    #         return (self.evaluationFunction(gameState),None)
    #     nextIndex=(index+1)%gameState.getNumAgents()
    #     if index==0:
    #         maxaction=None
    #         maxi=-99999
    #         self.depth-=1
    #         for i in gameState.getLegalActions(index):
    #             if (self.minimax(gameState.generateSuccessor(index,i),nextIndex)[0]>=maxi):
    #                 maxi=self.minimax(gameState.generateSuccessor(index,i),nextIndex)[0]
    #                 maxaction=i
    #         self.depth+=1
    #         return (maxi,maxaction)
    #     else:
    #         mini=99999
    #         for i in gameState.getLegalActions(index):
    #             mini=min(self.minimax(gameState.generateSuccessor(index,i),nextIndex)[0],mini)
    #         return (mini,None)

    def getAction(self, gameState: GameState):
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
        # self.depth=8
        # print(self.depth)
        # print(self.minimax(gameState,0)[1])
        def minimax(gameState: GameState,index):
            if (self.depth<=0 and index==0) or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState),None)
            nextIndex=(index+1)%gameState.getNumAgents()
            if index==0:
                maxaction=None
                maxi=-99999
                self.depth-=1
                for i in gameState.getLegalActions(index):
                    tmp=minimax(gameState.generateSuccessor(index,i),nextIndex)[0]
                    if (tmp>=maxi):
                        maxi=tmp
                        maxaction=i
                self.depth+=1
                return (maxi,maxaction)
            else:
                mini=99999
                for i in gameState.getLegalActions(index):
                    tmp=minimax(gameState.generateSuccessor(index,i),nextIndex)[0]
                    mini=min(tmp,mini)
                return (mini,None)
        return minimax(gameState,0)[1]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    # def Alpha_Beta(self,gameState: GameState,index,alpha,beta):
    #     if (self.depth<=0 and index==0) or gameState.isWin() or gameState.isLose():
    #         return (self.evaluationFunction(gameState),None)
    #     nextIndex=(index+1)%gameState.getNumAgents()
    #     if index==0:
    #         maxaction=None
    #         maxi=-99999
    #         self.depth-=1
    #         for i in gameState.getLegalActions(index):
    #             tmp=self.Alpha_Beta(gameState.generateSuccessor(index,i),nextIndex,alpha,beta)[0]
    #             if (tmp>=maxi):
    #                 maxi=tmp
    #                 maxaction=i
    #             alpha=max(alpha,tmp)
    #             if alpha>beta:
    #                 break
    #         self.depth+=1
    #         return (maxi,maxaction)
    #     else:
    #         mini=99999
    #         for i in gameState.getLegalActions(index):
    #             tmp=self.Alpha_Beta(gameState.generateSuccessor(index,i),nextIndex,alpha,beta)[0]
    #             mini=min(tmp,mini)
    #             beta=min(beta,mini)
    #             if alpha>beta:
    #                 break
    #         return (mini,None)
        
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def Alpha_Beta(gameState: GameState,index,alpha,beta):
            if (self.depth<=0 and index==0) or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState),None)
            nextIndex=(index+1)%gameState.getNumAgents()
            if index==0:
                maxaction=None
                maxi=-99999
                self.depth-=1
                for i in gameState.getLegalActions(index):
                    tmp=Alpha_Beta(gameState.generateSuccessor(index,i),nextIndex,alpha,beta)[0]
                    if (tmp>=maxi):
                        maxi=tmp
                        maxaction=i
                    alpha=max(alpha,tmp)
                    if alpha>beta:
                        break
                self.depth+=1
                return (maxi,maxaction)
            else:
                mini=99999
                for i in gameState.getLegalActions(index):
                    tmp=Alpha_Beta(gameState.generateSuccessor(index,i),nextIndex,alpha,beta)[0]
                    mini=min(tmp,mini)
                    beta=min(beta,mini)
                    if alpha>beta:
                        break
                return (mini,None)
        
        return Alpha_Beta(gameState,0,-99999,99999)[1]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def Expectimax(gameState: GameState,index):
            if (self.depth<=0 and index==0) or gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState),None)
            nextIndex=(index+1)%gameState.getNumAgents()
            if index==0:
                maxaction=None
                maxi=-99999
                self.depth-=1
                for i in gameState.getLegalActions(index):
                    tmp=Expectimax(gameState.generateSuccessor(index,i),nextIndex)[0]
                    if (tmp>=maxi):
                        maxi=tmp
                        maxaction=i
                self.depth+=1
                return (maxi,maxaction)
            else:
                sum=0.000
                count=0
                for i in gameState.getLegalActions(index):
                    count+=1
                    tmp=Expectimax(gameState.generateSuccessor(index,i),nextIndex)[0]
                    sum+=tmp
                sum/=count
                return (sum,None)
        return Expectimax(gameState,0)[1]
        util.raiseNotDefined()
def breadthfirstSearch(currentGameState: GameState):
    que=util.Queue()
    visited=set()
    Food = currentGameState.getFood()
    res=99999
    Pos=currentGameState.getPacmanPosition()
    que.push((Pos,0))
    visited.add(Pos)
    while not que.isEmpty():
        Pos,step=que.pop()
        # print(step)
        if Food[Pos[0]][Pos[1]]:
            res=step
            # print(step)
            return res
        for i in [(0,1),(0,-1),(1,0),(-1,0)]:
            # print(i)
            if (not currentGameState.hasWall(Pos[0]+i[0],Pos[1]+i[1])) and ((Pos[0]+i[0],Pos[1]+i[1]) not in visited):
                que.push(((Pos[0]+i[0],Pos[1]+i[1]),step+1))
                visited.add((Pos[0]+i[0],Pos[1]+i[1]))
    return res
# def mapmarix(currentGameState: GameState):
#         num=(currentGameState.walls.width)*(problem.walls.height)
#         matrix = [[9999 for _ in range(num)] for _ in range(num)]
#         for i in range(problem.walls.width):
#             for j in range(problem.walls.height):
#                 if problem.walls[i][j]:
#                     continue
#                 seq=i*(problem.walls.height)+j
#                 if i>0 and not problem.walls[i-1][j]:
#                     matrix[seq][(i-1)*(problem.walls.height)+j]=1
#                     matrix[(i-1)*(problem.walls.height)+j][seq]=1
#                 if j>0 and not problem.walls[i][j-1]:
#                     matrix[seq][i*(problem.walls.height)+j-1]=1
#                     matrix[i*(problem.walls.height)+j-1][seq]=1
#                 if i<problem.walls.width-1 and not problem.walls[i+1][j]:
#                     matrix[seq][(i+1)*(problem.walls.height)+j]=1
#                     matrix[(i+1)*(problem.walls.height)+j][seq]=1
#                 if j<problem.walls.height-1 and not problem.walls[i][j+1]:
#                     matrix[seq][i*(problem.walls.height)+j+1]=1
#                     matrix[i*(problem.walls.height)+j+1][seq]=1
#         for temp in range(num):
#             for i in range(num):
#                 for j in range(num):
#                     matrix[i][j]=min(matrix[i][j],matrix[i][temp]+matrix[temp][j])
#         problem.heuristicInfo['matrix']=matrix
def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    capsules=currentGameState.getCapsules()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    MinCapsule=99999
    if capsules.__len__()>0:
        for i in capsules:
            MinCapsule=min(MinCapsule,manhattanDistance(Pos, i))
    MaxFood=0
    MinFood=99999
    # print(Food.asList())
    if currentGameState.isWin():
        return 99999+10*currentGameState.getScore()
    for i in Food.asList():
        MaxFood=max(MaxFood,manhattanDistance(Pos, i))
        # MinFood=min(MinFood,manhattanDistance(Pos, i))
    MinFood=breadthfirstSearch(currentGameState)
    MinGhost= 99999
    for i in GhostStates:
        MinGhost=min(MinGhost,manhattanDistance(Pos, i.getPosition()))
    # print(ScaredTimes)
    totscare=0
    for i in ScaredTimes:
        totscare+=i
    score=-2*MinFood+20*currentGameState.getScore()+1000*totscare
    if(MinCapsule!=99999):
        score-=100*MinCapsule
    for i in ScaredTimes:
        if i>0:
            score-=10000*MinGhost
    if MinGhost<=2:
        return -1000
    if Food.asList().__len__()==0:
        return 99999+10*currentGameState.getScore()
    # print(score)
    # print(Pos)
    return score
    util.raiseNotDefined()
    
# Abbreviation
better = betterEvaluationFunction
