from Player import Player
from random import randrange, choice

class BetterAI(Player):
    """The class for Better AI"""

    def __init__(self, strToken, strName, lstBoard):
        Player.__init__(self, strToken, strName, lstBoard)

    def move(self):
        '''Better AI's move'''
        # slightly smarter than Super AI
        lstChoices = list()
        strOppositeToken = 'x'

        if self._strToken == 'x':
            strOppositeToken = 'o'
        else:
            strOppositeToken = 'x'

        # checking for available spots along the 0 column and 0 diagonally
        # adds availabilities to list of choices
        if self._lstBoard[0] is self._strToken:
            if self._lstBoard[3] is self._strToken and self._lstBoard[3] is not strOppositeToken and self._lstBoard[6] == ' ':
                lstChoices.append(6)
            elif self._lstBoard[3] == ' ':
                lstChoices.append(3)
            if self._lstBoard[4] is self._strToken and self._lstBoard[4] is not strOppositeToken and self._lstBoard[8] == ' ':
                lstChoices.append(8)
            elif self._lstBoard[4] == ' ':
                lstChoices.append(4)
        elif self._lstBoard[0] == ' ':
            lstChoices.append(0)
        # checking for available spots along the 1 column
        # adds availabilities to list of choices
        if self._lstBoard[1] is self._strToken:
            if self._lstBoard[4] is self._strToken and self._lstBoard[4] is not strOppositeToken and self._lstBoard[7] == ' ':
                lstChoices.append(7)
            elif self._lstBoard[4] == ' ' and 4 not in lstChoices:
                lstChoices.append(4)
        elif self._lstBoard[1] == ' ':
            lstChoices.append(1)
        # checking for available spots along the 2 column and 2 diagonally
        # adds availabilities to list of choices
        if self._lstBoard[2] is self._strToken:
            if self._lstBoard[5] is self._strToken and self._lstBoard[5] is not strOppositeToken and self._lstBoard[8] == ' ' and 8 not in lstChoices:
                lstChoices.append(8)
            elif self._lstBoard[3] == ' ' and 3 not in lstChoices:
                lstChoices.append(5)
            if self._lstBoard[4] is self._strToken and self._lstBoard[4] is not strOppositeToken and self._lstBoard[6] == ' ' and 6 not in lstChoices:
                lstChoices.append(6)
            elif self._lstBoard[4] == ' ' and 4 not in lstChoices:
                lstChoices.append(4)
        elif self._lstBoard[2] == ' ':
            lstChoices.append(2)
    
        # if lstChoices is empty return random number
        if len(lstChoices) == 0:
            for i in range(0, len(self._lstBoard), 1):
                if self._lstBoard[i] == ' ':
                    lstChoices.append(i)

        return choice(lstChoices)
        # return random number from choices
        return choice(lstChoices)