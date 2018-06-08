from random import randrange
from random import choice
from TicTacToe_OO import TicTacToe_OO

# static game data - doesn't change (hence immutable tuple data type)
WIN_SET = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), 
           (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

# global variables for game data
lstBoard = [' '] * 9
currentPlayer = '' # 'x' or 'o' for first and second player
players = {'x': 'Human', 'o': 'Human 2', 'x': 'Super AI', 'o': 'Super AI 2', 'x': 'Better AI', 'o': 'Better AI 2', 'x': 'Best AI',
           'o': 'Best AI 2'}
intPlayerOne = 0
intPlayerTwo = 0
playerOne = None
winner = None
move = None
intMoves = 0
blOO = True

# aesthetics...
HR = '-' * 40

# Game model functions
def checkMove():
    '''This function will return True if ``move`` is valid (in the board range 
    and free cell), or print an error message and return False if not valid. 
    ``move`` is an int board position [0..8].
    '''
    global move
    try:
        move = int(move)
        if lstBoard[move] == ' ':
            return True
        else:
            print('>> Sorry - that position is already taken!')
            return False
    except:
        print('>> %s is not a valid position! Must be int between 0 and 8.' % move)
        return False

def checkForResult():
    '''Checks the current board to see if there is a winner, tie or not.
    Returns a 'x' or 'o' to indicate a winner, 'tie' for a stale-mate game, or
    simply False if the game is still going.
    '''
    for row in WIN_SET:
        if lstBoard[row[0]] == lstBoard[row[1]] == lstBoard[row[2]] != ' ':
            return lstBoard[row[0]] # return an 'x' or 'o' to indicate winner

    if ' ' not in lstBoard:
        return 'tie'

    return None

# human or AI functions
def getHumanMove():
    '''Get a human players raw input. Returns None if a number is not entered.'''
    return input('[0-8] >> ')

def getAIMove():
    '''Get the AI's next move '''
    # A simple dumb random move - valid or NOT!
    # Note: It is the models responsibility to check for valid moves...
    return randrange(9) # [0..8]

def getBetterAIMove():
    '''Get the Better AI's next Move'''
    # slightly smarter than Super AI
    lstChoices = list()
    strOppositeToken = ''

    if currentPlayer == 'x':
        strOppositeToken = 'o'
    else:
        strOppositeToken = 'x'
    # checking for available spots along the 0 column and 0 diagonally
    # adds availabilities to list of choices
    if lstBoard[0] is currentPlayer:
        if lstBoard[3] is currentPlayer and lstBoard[3] is not strOppositeToken and lstBoard[6] == ' ':
            lstChoices.append(6)
        elif lstBoard[3] == ' ':
            lstChoices.append(3)
        if lstBoard[4] is currentPlayer and lstBoard[4] is not strOppositeToken and lstBoard[8] == ' ':
            lstChoices.append(8)
        elif lstBoard[4] == ' ':
            lstChoices.append(4)
    elif lstBoard[0] == ' ':
        lstChoices.append(0)
    # checking for available spots along the 1 column
    # adds availabilities to list of choices
    if lstBoard[1] is currentPlayer:
        if lstBoard[4] is currentPlayer and lstBoard[4] is not strOppositeToken and lstBoard[7] == ' ':
            lstChoices.append(7)
        elif lstBoard[4] == ' ' and 4 not in lstChoices:
            lstChoices.append(4)
    elif lstBoard[1] == ' ':
        lstChoices.append(1)
    # checking for available spots along the 2 column and 2 diagonally
    # adds availabilities to list of choices
    if lstBoard[2] is currentPlayer:
        if lstBoard[5] is currentPlayer and lstBoard[5] is not strOppositeToken and lstBoard[8] == ' ' and 8 not in lstChoices:
            lstChoices.append(8)
        elif lstBoard[3] == ' ' and 3 not in lstChoices:
            lstChoices.append(5)
        if lstBoard[4] is currentPlayer and lstBoard[4] is not strOppositeToken and lstBoard[6] == ' ' and 6 not in lstChoices:
            lstChoices.append(6)
        elif lstBoard[4] == ' ' and 4 not in lstChoices:
            lstChoices.append(4)
    elif lstBoard[2] == ' ':
        lstChoices.append(2)
    
    # if lstChoices is empty return random number
    if len(lstChoices) == 0:
        for i in range(0, len(lstBoard), 1):
            if lstBoard[i] == ' ':
                lstChoices.append(i)

        return choice(lstChoices)
    # return random number from choices
    return choice(lstChoices)

def getBestAIMove():
    '''Gets the next move for the best AI'''
    # Best AI
    # Turns 1 - 3 place token in corners. If on third turn can make winning move makes that move
    # On fourth turn chooses one of up to three winning moves. If end of method reached with no
    # possible moves places token in random available spot 
    lstChoices = list()
    global intMoves
    intMoves += 1

    if intMoves == 1:
        if lstBoard[0] == ' ':
            lstChoices.append(0)
        if lstBoard[2] == ' ':
            lstChoices.append(2)
        if lstBoard[6] == ' ':
            lstChoices.append(6)
        if lstBoard[8] == ' ':
            lstChoices.append(8)
    elif intMoves == 2:
        if lstBoard[0] == currentPlayer:
            if lstBoard[2] == ' ':
                lstChoices.append(2)
            if lstBoard[6] == ' ':
                lstChoices.append(6)
            if lstBoard[8] == ' ':
                lstChoices.append(8)
        elif lstBoard[2] == currentPlayer:
            if lstBoard[0] == ' ':
                lstChoices.append(0)
            if lstBoard[6] == ' ':
                lstChoices.append(6)
            if lstBoard[8] == ' ':
                lstChoices.append(8)
        elif lstBoard[6] == currentPlayer:
            if lstBoard[2] == ' ':
                lstChoices.append(2)
            if lstBoard[0] == ' ':
                lstChoices.append(0)
            if lstBoard[8] == ' ':
                lstChoices.append(8)
        elif lstBoard[8] == currentPlayer:
            if lstBoard[2] == ' ':
                lstChoices.append(2)
            if lstBoard[6] == ' ':
                lstChoices.append(6)
            if lstBoard[0] == ' ':
                lstChoices.append(0)
    elif intMoves == 3:
        if lstBoard[0] == currentPlayer:
            if lstBoard[2] == currentPlayer:
                if lstBoard[6] == ' ':
                    lstChoices.append(6)
                if lstBoard[8] == ' ':
                    lstChoices.append(8)
                if lstBoard[1] == ' ':
                    return 1
            if lstBoard[6] == currentPlayer:
                if lstBoard[2] == ' ':
                    lstChoices.append(2)
                if lstBoard[8] == ' ':
                    lstChoices.append(8)
                if lstBoard[3] == ' ':
                    return 3
            if lstBoard[8] == currentPlayer:
                if lstBoard[2] == ' ':
                    lstChoices.append(2)
                if lstBoard[6] == ' ':
                    lstChoices.append(6)
                if lstBoard[4] == ' ':
                    return 4
        elif lstBoard[2] == currentPlayer:
            if lstBoard[0] == currentPlayer:
                if lstBoard[6] == ' ':
                    lstChoices.append(6)
                if lstBoard[8] == ' ':
                    lstChoices.append(8)
                if lstBoard[1] == ' ':
                    return 1
            if lstBoard[6] == currentPlayer:
                if lstBoard[0] == ' ':
                    lstChoices.append(0)
                if lstBoard[8] == ' ':
                    lstChoices.append(8)
                if lstBoard[4] == ' ':
                    return 4
            if lstBoard[8] == currentPlayer:
                if lstBoard[0] == ' ':
                    lstChoices.append(0)
                if lstBoard[6] == ' ':
                    lstChoices.append(6)
                if lstBoard[5] == ' ':
                    return 5
        elif lstBoard[6] == currentPlayer:
            if lstBoard[2] == currentPlayer:
                if lstBoard[0] == ' ':
                    lstChoices.append(0)
                if lstBoard[8] == ' ':
                    lstChoices.append(8)
                if lstBoard[4] == ' ':
                    return 4
            elif lstBoard[0] == currentPlayer:
                if lstBoard[2] == ' ':
                    lstChoices.append(2)
                if lstBoard[8] == ' ':
                    lstChoices.append(8)
                if lstBoard[3] == ' ':
                    return 3
            elif lstBoard[8] == currentPlayer:
                if lstBoard[2] == ' ':
                    lstChoices.append(2)
                if lstBoard[0] == ' ':
                    lstChoices.append(0)
                if lstBoard[7] == ' ':
                    return 7
    elif intMoves == 4:
        if lstBoard[0] == currentPlayer and lstBoard[2] == currentPlayer and lstBoard[8] == currentPlayer:
            if lstBoard[1] == ' ':
                lstChoices.append(1)
            if lstBoard[4] == ' ':
                lstChoices.append(4)
            if lstBoard[5] == ' ':
                lstChoices.append(5)
        elif lstBoard[0] == currentPlayer and lstBoard[2] == currentPlayer and lstBoard[6] == currentPlayer:
            if lstBoard[1] == ' ':
                lstChoices.append(1)
            if lstBoard[3] == ' ':
                lstChoices.append(3)
            if lstBoard[4] == ' ':
                lstChoices.append(4)
        elif lstBoard[0] == currentPlayer and lstBoard[6] == currentPlayer and lstBoard[8] == currentPlayer:
            if lstBoard[3] == ' ':
                lstChoices.append(3)
            if lstBoard[4] == ' ':
                lstChoices.append(4)
            if lstBoard[7] == ' ':
                lstChoices.append(7)
        elif lstBoard[2] == currentPlayer and lstBoard[6] == currentPlayer and lstBoard[8] == currentPlayer:
            if lstBoard[4] == ' ':
                lstChoices.append(4)
            if lstBoard[5] == ' ':
                lstChoices.append(5)
            if lstBoard[7] == ' ':
                lstChoices.append(7)
    
    if len(lstChoices) == 0:
        for i in range(0, len(lstBoard), 1):
            if lstBoard[i] == ' ':
                lstChoices.append(i)

        return choice(lstChoices)
    else:
        return choice(lstChoices)

# Game Loop functions
def processInput():
    '''Get the current players next move.'''
    # save the next move into a global variable
    global move
    if currentPlayer == 'x':
        if intPlayerOne == 1:
            move = getHumanMove()
        elif intPlayerOne ==  2:
            move = getAIMove()
        elif intPlayerOne == 3:
            move = getBetterAIMove()
        else:
            move = getBestAIMove()
    else:
        if intPlayerTwo == 1:
            move = getHumanMove()
        elif intPlayerTwo ==  2:
            move = getAIMove()
        elif intPlayerTwo == 3:
            move = getBetterAIMove()
        else:
            move = getBestAIMove()

def updateModel():
    '''If the current players input is a valid move, update the board and check 
    the game model for a winning player. If the game is still going, change the
    current player and continue. If the input was not valid, let the player
    have another go.
    '''
    global winner, currentPlayer

    if checkMove():
        # do the new move which is stored in global move variable
        lstBoard[move] = currentPlayer
        # check board for winner
        winner = checkForResult()
        # change current player
        if currentPlayer == 'x':
            currentPlayer = 'o'
        else:
            currentPlayer = 'x'
    else:
        print('Try Again')

def renderBoard():
    '''Display the current game board to screen.'''
    print('    %s | %s | %s' % tuple(lstBoard[:3]))
    print('   -----------')
    print('    %s | %s | %s' % tuple(lstBoard[3:6]))
    print('   -----------')
    print('    %s | %s | %s' % tuple(lstBoard[6:]))

    # print the current player name
    if winner is None:
        print('The current player is %s' % players[currentPlayer])

def showHumanHelp():
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
    print(HR)


# Setup for each of the game types
# these methods set the player one to be human, Super AI or Better AI
def setupHuman():
    '''Setup for Human vs Super AI'''
    global playerOne
    playerOne = 0
    print('Human vs Super AI')

def setupSuper():
    '''Setup for Super AI vs Super AI'''
    global playerOne
    playerOne = 3
    print('Super AI vs Super AI')

def setupBetter():
    '''Setup for Better AI vs Super AI'''
    global playerOne
    playerOne = 2
    print('Better AI vs Super AI')

def playerOptions():
    return '1: Human\n2: Super AI\n3: Better AI\n4: Best AI'

def setup():
    global intPlayerOne, intPlayerTwo
    print('Player One:')
    print(playerOptions())
    intPlayerOne = int(input('Enter option: '))
    print('Player Two')
    print(playerOptions())
    intPlayerTwo = int(input('Enter option: '))

# main method
if __name__ == '__main__':
    if blOO:
        tttOO = TicTacToe_OO()
        tttOO.run()
    else:
        # Welcome ...
        print('Welcome to the amazing+awesome tic-tac-toe!')
        showHumanHelp()
        setup()

        # human player starts by default
        currentPlayer = 'x'

        # show initial board
        renderBoard()

        # Game loop
        while winner is None:
            processInput()
            updateModel()
            renderBoard()

        # print ending messages
        print(HR)
        if winner == 'tie':
            print('TIE!')
        elif winner in players:
            print('%s is the WINNER!!!' % players[winner])
        print(HR)    
        print('Game over. Goodbye')