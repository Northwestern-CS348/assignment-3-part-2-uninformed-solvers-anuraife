from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        pegs = ["peg1","peg2","peg3"]
        result = []
        
        for peg in pegs:
            ask = parse_input("fact: (on ?disk " + peg + ")")
            bindings = self.kb.kb_ask(ask)
            
            pegTuple = []
            
            if bindings:
                for binding in bindings:
                    disk = int(binding['?disk'][-1])
                    pegTuple.append(disk)
                pegTuple.sort()
            
            result.append(tuple(pegTuple))
        
        return tuple(result)
        
        
        

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if movable_statement.predicate == "movable":
            disk = str(movable_statement.terms[0])
            initialPeg = str(movable_statement.terms[1])
            finalPeg = str(movable_statement.terms[2])
            
            #disk is no longer on initial peg
            self.kb.kb_retract(parse_input("fact: (on " + disk + " " + initialPeg + ")"))

            #to be movable, disk must be on top of peg. It no longer is.
            self.kb.kb_retract(parse_input("fact: (top " + disk + " " + initialPeg + ")"))

            #There could either be a new top of the peg (which nothing is on top of now) OR the peg is empty
            newTop = self.kb.kb_ask(parse_input("fact: (onTop " + disk + " ?disk2)"))
            if newTop:
                self.kb.kb_retract(parse_input("fact: (onTop " + disk + " " + newTop[0]['?disk2'] + ")"))
                self.kb.kb_assert(parse_input("fact: (top " + newTop[0]['?disk2'] + " " + initialPeg + ")"))
            else:
                self.kb.kb_assert(parse_input("fact: (empty " + initialPeg + ")"))

            #now the disk is on the final peg
            self.kb.kb_assert(parse_input("fact: (on " + disk + " " + finalPeg + ")"))
            
            #the disk could now be onTop of the old top of the final peg OR the final peg is no longer empty
            oldTop = self.kb.kb_ask(parse_input("fact: (top ?disk " + finalPeg + ")"))
            if oldTop:
                self.kb.kb_retract(parse_input("fact: (top " + oldTop[0]['?disk'] + " " + finalPeg + ")"))
                self.kb.kb_assert(parse_input("fact: (onTop " + disk + " " + oldTop[0]['?disk'] + ")"))
            else:
                self.kb.kb_retract(parse_input("fact: (empty " + finalPeg + ")"))
            self.kb.kb_assert(parse_input("fact: (top " + disk + " " + finalPeg + ")"))

        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        rows = ["pos1", "pos2", "pos3"]
        result = []
        rowTuple = [0,0,0]
        for row in rows:
            ask = parse_input("fact: (position ?tile ?posx " + row + ")")
            bindings = self.kb.kb_ask(ask)
            if bindings:
                for binding in bindings:
                    tile = binding['?tile']
                    posx = int(binding['?posx'][-1])
                    if tile == "empty":
                        tileNum = -1
                    else:
                        tileNum = int(tile[-1])
                    rowTuple[posx-1] = tileNum
                result.append(tuple(rowTuple))
        
        return tuple(result)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if movable_statement.predicate == "movable":
            tile = str(movable_statement.terms[0])
            initPosx = str(movable_statement.terms[1])
            initPosy = str(movable_statement.terms[2])
            finalPosx = str(movable_statement.terms[3])
            finalPosy = str(movable_statement.terms[4])
            
            #tile is no longer at initial position
            self.kb.kb_retract(parse_input("fact: (position " + tile + " " + initPosx + " " + initPosy +")"))
            
            #the empty space has now moved
            self.kb.kb_retract(parse_input("fact: (position empty " + finalPosx + " " + finalPosy +")"))
            self.kb.kb_assert(parse_input("fact: (position empty " + initPosx + " " + initPosy +")"))
            
            #tile moved to final position
            self.kb.kb_assert(parse_input("fact: (position " + tile + " " + finalPosx + " " + finalPosy +")"))
            

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
