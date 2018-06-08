from Player import Player
from random import randrange, choice

class BestAI(Player):
    """Class handles Best AI"""
    
    def __init__(self, strToken, strName, lstBoard):
        Player.__init__(self, strToken, strName, lstBoard)

    def move(self):
        self._intTurns += 1
        lstChoices = list()

        if self._intTurns == 1:
            if self._lstBoard[0] == ' ':
                lstChoices.append(0)
            if self._lstBoard[2] == ' ':
                lstChoices.append(2)
            if self._lstBoard[6] == ' ':
                lstChoices.append(6)
            if self._lstBoard[8] == ' ':
                lstChoices.append(8)
        elif self._intTurns == 2:
            if self._lstBoard[0] == self._strToken:
                if self._lstBoard[2] == ' ':
                    lstChoices.append(2)
                if self._lstBoard[6] == ' ':
                    lstChoices.append(6)
                if self._lstBoard[8] == ' ':
                    lstChoices.append(8)
            elif self._lstBoard[2] == self._strToken:
                if self._lstBoard[0] == ' ':
                    lstChoices.append(0)
                if self._lstBoard[6] == ' ':
                    lstChoices.append(6)
                if self._lstBoard[8] == ' ':
                    lstChoices.append(8)
            elif self._lstBoard[6] == self._strToken:
                if self._lstBoard[2] == ' ':
                    lstChoices.append(2)
                if self._lstBoard[0] == ' ':
                    lstChoices.append(0)
                if self._lstBoard[8] == ' ':
                    lstChoices.append(8)
            elif self._lstBoard[8] == self._strToken:
                if self._lstBoard[2] == ' ':
                    lstChoices.append(2)
                if self._lstBoard[6] == ' ':
                    lstChoices.append(6)
                if self._lstBoard[0] == ' ':
                    lstChoices.append(0)
        elif self._intTurns == 3:
            if self._lstBoard[0] == self._strToken:
                if self._lstBoard[2] == self._strToken:
                    if self._lstBoard[6] == ' ':
                        lstChoices.append(6)
                    if self._lstBoard[8] == ' ':
                        lstChoices.append(8)
                    if self._lstBoard[1] == ' ':
                        return 1
                if self._lstBoard[6] == self._strToken:
                    if self._lstBoard[2] == ' ':
                        lstChoices.append(2)
                    if self._lstBoard[8] == ' ':
                        lstChoices.append(8)
                    if self._lstBoard[3] == ' ':
                        return 3
                if self._lstBoard[8] == self._strToken:
                    if self._lstBoard[2] == ' ':
                        lstChoices.append(2)
                    if self._lstBoard[6] == ' ':
                        lstChoices.append(6)
                    if self._lstBoard[4] == ' ':
                        return 4
            elif self._lstBoard[2] == self._strToken:
                if self._lstBoard[0] == self._strToken:
                    if self._lstBoard[6] == ' ':
                        lstChoices.append(6)
                    if self._lstBoard[8] == ' ':
                        lstChoices.append(8)
                    if self._lstBoard[1] == ' ':
                        return 1
                if self._lstBoard[6] == self._strToken:
                    if self._lstBoard[0] == ' ':
                        lstChoices.append(0)
                    if self._lstBoard[8] == ' ':
                        lstChoices.append(8)
                    if self._lstBoard[4] == ' ':
                        return 4
                if self._lstBoard[8] == self._strToken:
                    if self._lstBoard[0] == ' ':
                        lstChoices.append(0)
                    if self._lstBoard[6] == ' ':
                        lstChoices.append(6)
                    if self._lstBoard[5] == ' ':
                        return 5
            elif self._lstBoard[6] == self._strToken:
                if self._lstBoard[2] == self._strToken:
                    if self._lstBoard[0] == ' ':
                        lstChoices.append(0)
                    if self._lstBoard[8] == ' ':
                        lstChoices.append(8)
                    if self._lstBoard[4] == ' ':
                        return 4
                elif self._lstBoard[0] == self._strToken:
                    if self._lstBoard[2] == ' ':
                        lstChoices.append(2)
                    if self._lstBoard[8] == ' ':
                        lstChoices.append(8)
                    if self._lstBoard[3] == ' ':
                        return 3
                elif self._lstBoard[8] == self._strToken:
                    if self._lstBoard[2] == ' ':
                        lstChoices.append(2)
                    if self._lstBoard[0] == ' ':
                        lstChoices.append(0)
                    if self._lstBoard[7] == ' ':
                        return 7
        elif self._intTurns == 4:
            if self._lstBoard[0] == self._strToken and self._lstBoard[2] == self._strToken and self._lstBoard[8] == self._strToken:
                if self._lstBoard[1] == ' ':
                    lstChoices.append(1)
                if self._lstBoard[4] == ' ':
                    lstChoices.append(4)
                if self._lstBoard[5] == ' ':
                    lstChoices.append(5)
            elif self._lstBoard[0] == self._strToken and self._lstBoard[2] == self._strToken and self._lstBoard[6] == self._strToken:
                if self._lstBoard[1] == ' ':
                   lstChoices.append(1)
                if self._lstBoard[3] == ' ':
                   lstChoices.append(3)
                if self._lstBoard[4] == ' ':
                   lstChoices.append(4)
            elif self._lstBoard[0] == self._strToken and self._lstBoard[6] == self._strToken and self._lstBoard[8] == self._strToken:
                if self._lstBoard[3] == ' ':
                   lstChoices.append(3)
                if board[4] == ' ':
                   lstChoices.append(4)
                if self._lstBoard[7] == ' ':
                    lstChoices.append(7)
            elif self._lstBoard[2] == self._strToken and self._lstBoard[6] == self._strToken and self._lstBoard[8] == self._strToken:
                if self._lstBoard[4] == ' ':
                    lstChoices.append(4)
                if self._lstBoard[5] == ' ':
                    lstChoices.append(5)
                if self._lstBoard[7] == ' ':
                    lstChoices.append(7)
    
        if len(lstChoices) == 0:
            for i in range(0, len(self._lstBoard), 1):
                if self._lstBoard[i] == ' ':
                    lstChoices.append(i)

            return choice(lstChoices)
        else:
            return choice(lstChoices)