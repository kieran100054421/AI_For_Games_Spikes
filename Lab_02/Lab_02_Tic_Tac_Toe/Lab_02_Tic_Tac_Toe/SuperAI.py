from Player import Player
from random import randrange

class SuperAI(Player):
    """Class handling the Super AI"""

    # initialiser
    def __init__(self, strToken, strName, lstBoard):
       Player.__init__(self, strToken, strName, lstBoard)

    def move(self):
        '''A simple dumb random move - valid or NOT!'''
        self._intTurns += 1
        return randrange(9)