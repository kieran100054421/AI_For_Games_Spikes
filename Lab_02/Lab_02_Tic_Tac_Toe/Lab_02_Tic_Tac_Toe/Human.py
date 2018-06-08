from Player import Player

class Human(Player):
    """Human controlled Player"""

    def __init__(self, strToken, strName, lstBoard):
        Player.__init__(self, strToken, strName, lstBoard)

    def move(self):
        '''Human player's move'''
        return input('[0-8] >> ')