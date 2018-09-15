import enum
import numpy as np

# noinspection PyArgumentList
Winner = enum.Enum("Winner", "X O draw")

# noinspection PyArgumentList
Player = enum.Enum("Player", "X O")

# Map from action(interger from 1 to 9) to position on the board(tuples of row and column)
action_mapping = {1:(0,0),2:(0,1),3:(0,2),4:(1,0),5:(1,1),6:(1,2),7:(2,0),8:(2,1),9:(2,2)}
position_mapping = {(0,0):1,(0,1):2,(0,2):3,(1,0):4,(1,1):5,(1,2):6,(2,0):7,(2,1):8,(2,2):9}

class Env:
    def __init__(self):
        self.board = None
        self.turn = 0
        self.done = False
        self.winner = None  # type: Winner
        self.size = 3

    def reset(self):
        self.board = []
        for i in range(self.size):
            self.board.append([])
            for j in range(self.size):
                self.board[i].append(' ')
        self.turn = 0
        self.done = False
        self.winner = None
        return self

    def update(self, board):
        self.board = np.copy(board)
        self.turn = self.turn_n()
        self.done = False
        self.winner = None
        return self

    def turn_n(self):
        '''
        Counts how many turns have passed in the current game's state
        '''
        turn = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != ' ':
                    turn += 1
        return turn

    def player_turn(self):
        '''
        Returns a Player Object to specify whose turn is it
        '''
        if self.turn % 2 == 0:
            return Player.O
        else:
            return Player.X

    def step(self, action):
        '''
        Parameters:
        action: an interger (from 1 to 9) to represent which space the player want to place in.
        '''
        while(action is None or action < 1 or action > 9):
            raise InputError

        row, column = action_mapping[action]
        self.board[row][column] = ('X' if self.player_turn() == Player.X else 'O')

        self.turn += 1
        self.check_for_three()

        if self.turn >= 9:
            self.done = True
            if self.winner is None:
                self.winner = Winner.draw

        return self.board, {}

    def legal_moves(self):
        '''
        Returns a list of legal moves (from 1 to 9)
        '''
        legal = []
        for j in range(self.size):
            for i in range(self.size):
                if self.board[i][j] == ' ':
                    legal.append(position_mapping[(i,j)])
        return legal

    def check_for_three(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.vertical_check(i, j):
                        self.done = True
                        return

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontal_check(i, j):
                        self.done = True
                        return

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    diag_fours = self.diagonal_check()
                    if diag_fours:
                        self.done = True
                        return

    def vertical_check(self, row, col):
        three_in_a_row = False
        consecutive_count = 0

        for i in range(row, self.size):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break

        if consecutive_count == 3:
            three_in_a_row = True
            if 'x' == self.board[row][col].lower():
                self.winner = Winner.X
            else:
                self.winner = Winner.O

        return three_in_a_row

    def horizontal_check(self, row, col):
        three_in_a_row = False
        consecutive_count = 0

        for j in range(col, self.size):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break

        if consecutive_count == 3:
            three_in_a_row = True
            if 'x' == self.board[row][col].lower():
                self.winner = Winner.X
            else:
                self.winner = Winner.O

        return three_in_a_row

    def diagonal_check(self):
        if self.board[1][1].lower() == ' ':
            return False

        three_in_a_row = False
        if self.board[0][0].lower() == self.board[1][1].lower() == self.board[2][2].lower() or \
        self.board[0][2].lower() == self.board[1][1].lower() == self.board[2][0].lower():
            three_in_a_row = True
            if 'x' == self.board[1][1].lower():
                self.winner = Winner.X
            else:
                self.winner = Winner.O

        return three_in_a_row

    def X_and_O_plane(self):
        '''
        Returns board representation of X plane and O plane. An X plane will have a value 1 where
        X is present and 0 when there is nothing.
        '''
        board_O = np.copy(self.board)
        board_X = np.copy(self.board)
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ':
                    board_O[i][j] = 0
                    board_X[i][j] = 0
                elif self.board[i][j] == 'O':
                    board_O[i][j] = 1
                    board_X[i][j] = 0
                else:
                    board_O[i][j] = 0
                    board_X[i][j] = 1
        return np.array(board_O), np.array(board_X)

    def render(self):
        print("\nRound: " + str(self.turn))

        for i in range(self.size):
            print("\t", end=" ")
            for j in range(self.size):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")

        if self.done:
            print("Game Over!")
            if self.winner == Winner.X:
                print("X is the winner")
            elif self.winner == Winner.O:
                print("O is the winner")
            else:
                print("Game was a draw")

    @property
    def observation(self):
        return ''.join(''.join(x for x in y) for y in self.board)