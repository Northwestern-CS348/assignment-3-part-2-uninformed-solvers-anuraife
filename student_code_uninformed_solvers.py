from solver import *
import queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        
        #if we're already at the victory condition, just return true
        if self.currentState.state == self.victoryCondition:
            return True
        
        moves = self.gm.getMovables()
        curr = self.currentState
        self.visited[curr] = True
        
        #if there are moves to make, populate curr's children array
        if moves:
            for move in moves:
                self.gm.makeMove(move)
                childState = GameState(self.gm.getGameState(), curr.depth + 1, move) 
                childState.parent = curr
                self.gm.reverseMove(move)
                curr.children.append(childState)
            #visit each child
            for child in curr.children:
                if child not in self.visited:
                    self.visited[child] = True
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child
                    return self.currentState.state == self.victoryCondition
        #go back up the tree
        self.gm.reverseMove(self.currentState.requiredMovable)
        self.currentState = self.currentState.parent
        return False

    
class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.nodes = queue.Queue()
        self.path = dict()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """

        if self.currentState.state == self.victoryCondition:
            return True
        
        moves = self.gm.getMovables()
        curr = self.currentState
        self.visited[curr] = True
        
        #at depth of 0, path to root is empty
        if curr.depth == 0:
            self.path[curr] = []
        
        #if there are moves to make, put each child in the queue and build a path from root to child
        if moves:
            for move in moves:
                self.gm.makeMove(move)
                childState = GameState(self.gm.getGameState(), curr.depth + 1, move)
                if childState not in self.visited:
                    self.visited[childState] = True
                    self.nodes.put(childState)
                    self.path[childState] = self.path[curr].copy()
                    self.path[childState].append(childState)
                self.gm.reverseMove(move)
        
        #path from current node back to root, reverse all moves to get back to parent
        prevNodes = self.path[self.currentState]
        prevNodes.reverse()
        
        #path to next node (top of the queue), make all moves to get to child
        self.currentState = self.nodes.get()
        nextNodes = self.path[self.currentState]        

        for node in prevNodes:
            self.gm.reverseMove(node.requiredMovable)

        for node in nextNodes:
            self.gm.makeMove(node.requiredMovable)

        if self.currentState.state == self.victoryCondition:
            return True

        else:
            return False

        