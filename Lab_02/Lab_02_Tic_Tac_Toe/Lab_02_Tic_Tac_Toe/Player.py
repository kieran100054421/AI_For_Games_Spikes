from random import randrange

class Player(object):
    """Base Class for all AI and Human Players"""

    # 'private' variables
    _strToken = ''
    _strName = ''
    _intTurns = 0
    _lstBoard = []

    # initialiser
    def __init__(self, strToken, strName, lstBoard):
        self._strToken = strToken
        self._strName = strName
        self._lstBoard = lstBoard

    def move(self):
        '''Base move for all players'''
        self._intTurns += 1
        return randrange(9)

    # getters
    def getName(self):
        '''Gets the players name'''
        return self._strName

    def getToken(self):
        '''Gets the players token'''
        return self._strToken