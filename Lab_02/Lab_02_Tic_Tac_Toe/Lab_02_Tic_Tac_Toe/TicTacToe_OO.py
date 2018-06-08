from random import randrange
from SuperAI import SuperAI
from BetterAI import BetterAI
from BestAI import BestAI
from Human import Human

class TicTacToe_OO(object):
    """Object Oriented version of Tic Tac Toe"""

    # Class Variables
    WIN_SET = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), 
        (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)
    )
    
    lstBoard = []
    lstPlayers = []
    strCurrentPlayer = ''
    HR = ''
    winner = None
    strMove = ''
    
    def __init__(self):
        self.lstBoard = [' '] * 9
        self.HR = '-' * 40
        self.winner = None
        self.strCurrentPlayer = 'x'

    def checkMove(self):
        '''This function will return True if ``move`` is valid (in the board range 
        and free cell), or print an error message and return False if not valid. 
        ``move`` is an int board position [0..8].
        '''
        try:
            self.strMove = int(self.strMove)
            if self.lstBoard[self.strMove] == ' ':
                return True
            else:
                print('>> Sorry - that position is already taken!')
                return False
        except:
            print('>> %s is not a valid position! Must be int between 0 and 8.' % self.strMove)
            return False

    def checkForResult(self):
        '''Checks the current board to see if there is a winner, tie or not.
        Returns a 'x' or 'o' to indicate a winner, 'tie' for a stale-mate game, or
        simply False if the game is still going.
        '''
        for row in self.WIN_SET:
            if self.lstBoard[row[0]] == self.lstBoard[row[1]] == self.lstBoard[row[2]] != ' ':
                return self.lstBoard[row[0]] # return an 'x' or 'o' to indicate winner

        if ' ' not in self.lstBoard:
            return 'tie'

        return None

    def processInput(self):
        '''Get the current players next move.'''
        # save the next move into a global variable
        if self.strCurrentPlayer == 'x':
            self.strMove = self.lstPlayers[0].move()
        else:
            self.strMove = self.lstPlayers[1].move()
        
    def updateModel(self):
        '''If the current players input is a valid move, update the board and check 
        the game model for a winning player. If the game is still going, change the
        current player and continue. If the input was not valid, let the player
        have another go.
        '''

        if self.checkMove():
            # do the new move which is stored in global move variable
            self.lstBoard[self.strMove] = self.strCurrentPlayer
            # check board for winner
            self.winner = self.checkForResult()
            # change current player
            if self.strCurrentPlayer == 'x':
                self.strCurrentPlayer = 'o'
            else:
                self.strCurrentPlayer = 'x'
        else:
            print('Try Again')

    def renderBoard(self):
        '''Display the current game board to screen.'''
        print('    %s | %s | %s' % tuple(self.lstBoard[:3]))
        print('   -----------')
        print('    %s | %s | %s' % tuple(self.lstBoard[3:6]))
        print('   -----------')
        print('    %s | %s | %s' % tuple(self.lstBoard[6:]))

        # print the current player name
        if self.winner is None:
            if self.strCurrentPlayer is self.lstPlayers[0].getToken():
                print('The current player is ' + self.lstPlayers[0].getName())
            else:
                print('The current player is ' + self.lstPlayers[1].getName())

    def showHumanHelp(self):
        '''Show the player help/instructions. '''
        tmp = '''
    To make a move enter a number between 0 - 8 and press enter.  
    The number corresponds to a board position as illustrated:

        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
        '''
        print(tmp)
        print(self.HR)
        
    def playerOptions():
         return '1: Human\n2: Super AI\n3: Better AI\n4: Best AI'

    def setup(self):
        '''Setups player one and two'''
        for i in range(0, 2, 1):
            print('1: Human\n2: Super AI\n3: Better AI\n4: Best AI')
            intAI = int(input('Enter AI Option: '))
            strName = ''

            if i == 0:
                if intAI == 1:
                    strName = 'Human'
                    self.lstPlayers.append(Human('x', strName, self.lstBoard))
                elif intAI == 2:
                    strName = 'Super AI'
                    self.lstPlayers.append(SuperAI('x', strName, self.lstBoard))
                elif intAI == 3:
                    strName = 'Better AI'
                    self.lstPlayers.append(BetterAI('x', strName, self.lstBoard))
                elif intAI == 4:
                    strName = 'Best AI'
                    self.lstPlayers.append(BestAI('x', strName, self.lstBoard))
            elif i == 1:
                if intAI == 1:
                    strName = 'Human ' + str(i + 1)
                    self.lstPlayers.append(Human('o', strName, self.lstBoard))
                elif intAI == 2:
                    strName = 'Super AI ' + str(i + 1)
                    self.lstPlayers.append(SuperAI('o', strName, self.lstBoard))
                elif intAI == 3:
                    strName = 'Better AI ' + str(i + 1)
                    self.lstPlayers.append(BetterAI('o', strName, self.lstBoard))
                elif intAI == 4:
                    strName = 'Best AI ' + str(i + 1)
                    self.lstPlayers.append(BestAI('o', strName, self.lstBoard))

    def run(self):
        '''Runs Tic Tac Toe Game'''
        print('Welcome to the amazing+awesome tic-tac-toe!')
        self.setup()
        self.showHumanHelp()
        self.renderBoard()

        while self.winner is None:
            self.processInput()
            self.updateModel()
            self.renderBoard()

        print(self.HR)
        if self.winner == 'tie':
            print('TIE!')
        else:
            if self.winner is self.lstPlayers[0].getToken():
                print(self.lstPlayers[0].getName() + ' is the WINNER!!!')
            else:
                print(self.lstPlayers[1].getName() + ' is the WINNER!!!')
        print(self.HR)    
        print('Game over. Goodbye')