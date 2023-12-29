from copy import deepcopy
from math import inf


class Position(object):

    def __init__(self, table, white_to_move=True):
        self._table = table
        self._next_moves = None
        self._game_end = False
        self._white_to_move = white_to_move
        self._evaluation = 0

    def __gt__(self, other):
        return self._evaluation > other.get_evaluation()

    def __ge__(self, other):
        return self._evaluation >= other.get_evaluation()

    def __le__(self, other):
        return self._evaluation <= other.get_evaluation()

    def __lt__(self, other):
        return self._evaluation < other.get_evaluation()

    def __eq__(self, other):
        return self._evaluation == other.get_evaluation()

    def get_game_end(self):
        return self._game_end

    def set_white_to_move(self, value):
        self._white_to_move = value

    def get_white_to_move(self):
        return self._white_to_move

    def set_evaluation(self, new_eval):
        self._evaluation = new_eval

    def get_next_moves(self, forced=False):
        if self._next_moves is None:
            self.generate_next_moves(forced)
        return self._next_moves

    def get_evaluation(self):
        return self._evaluation

    def get_table(self):
        return self._table

    def count_pieces(self):
        num_white = 0
        num_black = 0
        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._table[i][j] == 'x':
                    num_white += 1
                if self._table[i][j] == 'X':
                    num_white += 1
                if self._table[i][j] == 'o':
                    num_black += 1
                if self._table[i][j] == 'O':
                    num_black += 1
        return num_white, num_black

    def find_move_played(self, previous):
        move = []
        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._table[i][j] != previous[i][j]:
                    move.append((i, j))

        return move

    def evaluate_state_ending(self):
        """
        Basic heuristic that only counts the piece value

        """
        white_value = 0
        black_value = 0
        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._table[i][j] == 'x':
                    white_value += 1
                if self._table[i][j] == 'X':
                    white_value += 2
                if self._table[i][j] == 'o':
                    black_value += 1
                if self._table[i][j] == 'O':
                    black_value += 2
        self._evaluation = black_value - white_value
        return self._evaluation

    def find_capturing_moves(self):
        capt_pieces = []
        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._white_to_move and (self._table[i][j] == 'x' or self._table[i][j] == 'X'):
                    moves = self.find_valid_moves_for_piece((i, j))
                    for move in moves:
                        if i - move[0] == 2 or i - move[0] == -2 or abs(i-move[0]) == 4 or i-move[0] == 0:
                            capt_pieces.append((i, j))
                            break
                if not self._white_to_move and (self._table[i][j] == 'o' or self._table[i][j] == 'O'):
                    moves = self.find_valid_moves_for_piece((i, j))
                    for move in moves:
                        if i - move[0] == 2 or i - move[0] == -2 or abs(i-move[0]) == 4 or i-move[0] == 0:
                            capt_pieces.append((i, j))
                            break
        return capt_pieces

    def evaluate_state(self):
        """
        Still a basic heuristic but it takes into account piece position as well as the piece value
        
        """
        white_value = 0
        black_value = 0
        num_white = 0
        num_black = 0

        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._table[i][j] == 'x':
                    num_white += 1
                    if 2 < i < 5 and 1 < j < 6:  # kontrola centra
                        white_value += 5
                    elif i < 4:
                        white_value += 4.5
                    else:
                        white_value += 4
                if self._table[i][j] == 'X':
                    num_white += 1
                    white_value += 6
                if self._table[i][j] == 'o':
                    num_black += 1
                    if 2 < i < 5 and 1 < j < 6:  # kontrola centra
                        black_value += 5
                    elif i > 3:
                        black_value += 4.5
                    else:
                        black_value += 4
                if self._table[i][j] == 'O':
                    num_black += 1
                    black_value += 6

        self._evaluation = black_value - white_value

        if num_white == 0:
            self._evaluation = inf
            self._game_end = True
        if num_black == 0:
            self._evaluation = -inf
            self._game_end = True
        return self._evaluation

    def heuristic(self):
        # number of regular pawn (1)
        # number of king (2)
        # number piece in back row (3) 
        # number of piece in middle 4 cols of middle 2 rows (4) 
        # number of piece in middle 4 cols but not middle 2 rows (5)
        # number of pieces that can be taken by the opponent (6)
        # number of pieces that cannot be taken until pieces behind it are moved (7)

        w1, b1, w2, b2  = 0,0,0,0
        w3,b3,w4,b4,w5,b5,w6,b6,w7,b7 = 0,0,0,0,0,0,0,0,0,0
        black_value = 0
        white_value = 0
        table = self._table

        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if table[i][j] == "x":
                    w1 += 1
                    if i == 7:
                        w3 += 1
                    if 1<j<6:
                        if 2<i<5:
                            w4 += 1
                        else:
                            w5 += 1
                    if 0<i<7 and 0<j<7:
                        if (table[i-1][j+1].lower() == "o"):
                            if table[i+1][j-1] == ".":
                                w6 += 1
                            elif table[i+1][j-1].lower() == "x":
                                w7 += 1
                        if (table[i-1][j-1].lower() == "o"):
                            if table[i+1][j+1] == ".":
                                w6 += 1
                            elif table[i+1][j+1].lower() == "x":
                                w7 += 1
                        if table[i+1][j-1] == "O":
                            if table[i-1][j+1] == ".":
                                w6 += 1
                            elif table[i-1][j+1].lower() == "x":
                                w7 += 1
                        if table[i+1][j+1] == "O":
                            if table[i-1][j-1] == ".":
                                w6 += 1
                            elif table[i-1][j-1].lower() == "x":
                                w7 += 1

                if table[i][j] == "X":
                    w2 += 1
                    if i == 7:
                        w3 += 1
                    if 1<j<6:
                        if 2<i<5:
                            w4 += 1
                        else:
                            w5 += 1
                    if 0<i<7 and 0<j<7:
                        if (table[i-1][j+1].lower() == "o"):
                            if table[i+1][j-1] == ".":
                                w6 += 1
                            elif table[i+1][j-1].lower() == "x":
                                w7 += 1
                        if (table[i-1][j-1].lower() == "o"):
                            if table[i+1][j+1] == ".":
                                w6 += 1
                            elif table[i+1][j+1].lower() == "x":
                                w7 += 1
                        if table[i+1][j-1] == "O":
                            if table[i-1][j+1] == ".":
                                w6 += 1
                            elif table[i-1][j+1].lower() == "x":
                                w7 += 1
                        if table[i+1][j+1] == "O":
                            if table[i-1][j-1] == ".":
                                w6 += 1
                            elif table[i-1][j-1].lower() == "x":
                                w7 += 1
                    
                if table[i][j] == "o":
                    b1 += 1
                    if i == 0:
                        b3 += 1
                    if 1<j<6:
                        if 2<i<5:
                            b4 += 1
                        else:
                            b5 += 1
                    if 0<i<7 and 0<j<7:
                        if (table[i+1][j+1].lower() == "x"):
                            if table[i-1][j-1] == ".":
                                b6 += 1
                            elif table[i-1][j-1].lower() == "o":
                                b7 += 1
                        if (table[i+1][j-1].lower() == "o"):
                            if table[i-1][j+1] == ".":
                                b6 += 1
                            elif table[i-1][j+1].lower() == "o":
                                b7 += 1    
                        if table[i-1][j-1] == "X":
                            if table[i+1][j+1] == ".":
                                b6 += 1
                            elif table[i-1][j+1].lower() == "o":
                                b7 += 1
                        if table[i-1][j+1] == "X":
                            if table[i+1][j-1] == ".":
                                b6 += 1
                            elif table[i+1][j-1].lower() == "o":
                                b7 += 1

                if table[i][j] == "O":
                    b2 += 1
                    if i == 0:
                        b3 += 1
                    if 1<j<6:
                        if 2<i<5:
                            b4 += 1
                        else:
                            b5 += 1
                    if 0<i<7 and 0<j<7:
                        if (table[i+1][j+1].lower() == "x"):
                            if table[i-1][j-1] == ".":
                                b6 += 1
                            elif table[i-1][j-1].lower() == "o":
                                b7 += 1
                        if (table[i+1][j-1].lower() == "o"):
                            if table[i-1][j+1] == ".":
                                b6 += 1
                            elif table[i-1][j+1].lower() == "o":
                                b7 += 1    
                        if table[i-1][j-1] == "X":
                            if table[i+1][j+1] == ".":
                                b6 += 1
                            elif table[i-1][j+1].lower() == "o":
                                b7 += 1
                        if table[i-1][j+1] == "X":
                            if table[i+1][j-1] == ".":
                                b6 += 1
                            elif table[i+1][j-1].lower() == "o":
                                b7 += 1
                    
        black_value += 5*b1 + 7.75*b2 + 4*b3 + 2.5*b4 + 0.5*b5 + -3*b6 + 3*b7
        white_value += 5*w1 + 7.75*w2 + 4*w3 + 2.5*w4 + 0.5*w5 + -3*w6 + 3*w7
        self._evaluation = black_value - white_value
        if w1+w2 == 0:
            self._evaluation = inf
            self._game_end = True
        if b1+b2 == 0:
            self._evaluation = -inf
            self._game_end = True
        
        return self._evaluation        


    def generate_next_moves(self, forced=False):
        self._next_moves = []
        captures = []
        all_moves = []

        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._white_to_move:
                    if self._table[i][j] == "x" or self._table[i][j] == "X":
                        valid_moves = self.find_valid_moves_for_piece(
                            (i, j), forced)
                        for move in valid_moves:
                            if move[0] - i == 2 or move[0] - i == -2 or move[0] - i == 4 or move[0] - i == -4 or move[0] - i == 0:
                                new_table = self.generate_new_state(
                                    (i, j), move)
                                position = Position(
                                    new_table, not self._white_to_move)
                                captures.append(position)
                
                            else:
                                new_table = self.generate_new_state(
                                    (i, j), move)
                                position = Position(
                                    new_table, not self._white_to_move)
                                all_moves.append(position)

                else:
                    if self._table[i][j] == "o" or self._table[i][j] == "O":
                        valid_moves = self.find_valid_moves_for_piece(
                            (i, j), forced)
                        for move in valid_moves:
                            if move[0] - i == 2 or move[0] - i == -2 or move[0] - i == 4 or move[0] - i == -4:
                                new_table = self.generate_new_state(
                                    (i, j), move)
                                position = Position(
                                    new_table, not self._white_to_move)
                                captures.append(position)
                            else:
                                new_table = self.generate_new_state(
                                    (i, j), move)
                                position = Position(
                                    new_table, not self._white_to_move)
                                all_moves.append(position)
        if forced and len(captures) > 0:
            self._next_moves = captures
        else:
            self._next_moves = captures + all_moves

    def generate_new_state(self, figure, move):
        table_copy = deepcopy(self._table)
        figure_type = table_copy[figure[0]][figure[1]]
        if table_copy[move[0]][move[1]] == ".":
            if figure_type == "x" or figure_type == "X":
                if move[0] == 0:  
                    table_copy[figure[0]][figure[1]] = 'X'
                    
                if figure[0] - move[0] == 2 or figure[0] - move[0] == -2:
                    row = figure[0] + (move[0] - figure[0]) // 2
                    column = figure[1] + (move[1] - figure[1]) // 2
                    table_copy[row][column] = "."

                if figure[0] - move[0] == 4: # double jump up
                    row1 = figure[0] - 1
                    row2 = figure[0] - 3

                    if figure[1] - move[1] == 0: # ziczac 
                        if figure[1] + 2 < 8: # right first
                            if table_copy[figure[0]-2][figure[1]+2] == "." and table_copy[figure[0]-1][figure[1]+1].lower() == "o":
                                col = figure[1] + 1
                                table_copy[row1][col] = "."
                                table_copy[row2][col] = "."
                        if figure[1] - 2 >= 0: # left first
                            if table_copy[figure[0]-2][figure[1]-2] == "." and table_copy[figure[0]-1][figure[1]-1].lower() == "o":
                                col = figure[1] - 1
                                table_copy[row1][col] = "."
                                table_copy[row2][col] = "."

                    elif figure[1] - move[1] == 4: # left double jump
                        col1 = figure[1] - 1
                        col2 = figure[1] - 3
                        table_copy[row1][col1] = "."
                        table_copy[row2][col2] = "."
                    elif figure[1] - move[1] == -4: # right double jump
                        col1 = figure[1] + 1
                        col2 = figure[1] + 3
                        table_copy[row1][col1] = "."
                        table_copy[row2][col2] = "."

                if figure[0] - move[0] == -4: # double jump down
                    row1 = figure[0] + 1
                    row2 = figure[0] + 3
                    if figure[1] - move[1] == 0: # ziczac
                        
                        if figure[1] + 2 < 8: # right first
                            if figure[0]+2 < 8 and figure[1]+2 < 8:
                                if table_copy[figure[0]+2][figure[1]+2] == "." and table_copy[figure[0]+1][figure[1]+1].lower() == "o":
                                    
                                    col = figure[1] + 1
                                    table_copy[row1][col] = "."
                                    table_copy[row2][col] = "."
                        if figure[1] - 2 >= 0:
                            if figure[0]+2 < 8 and figure[1]-2 >= 0:
                                if table_copy[figure[0]+2][figure[1]-2] == "." and table_copy[figure[0]+1][figure[1]-1].lower() == "o":
                                    col = figure[1] - 1
                                    table_copy[row1][col] = "."
                                    table_copy[row2][col] = "."
                    elif figure[1] - move[1] == 4: # left double jump
                        col1 = figure[1] - 1
                        col2 = figure[1] - 3
                        table_copy[row1][col1] = "."
                        table_copy[row2][col2] = "."
                    elif figure[1] - move[1] == -4: # right double jump
                        col1 = figure[1] + 1
                        col2 = figure[1] + 3
                        table_copy[row1][col1] = "."
                        table_copy[row2][col2] = "."
                
                if figure[0] - move[0] == 0:
                    if figure[1] - move[1] == 4: # double jump left
                        col1 = figure[1] - 1
                        col2 = figure[1] - 3
                        if figure[0] - 2 >= 0:
                            if table_copy[figure[0]-1][col1].lower() == "o" and table_copy[figure[0]-2][figure[1]-2] == "." and table_copy[figure[0]-1][col2]=="o":
                                row = figure[0] -1
                                table_copy[row][col1] = "."
                                table_copy[row][col2] = "."
                        if figure[0] + 2 < 8:
                            if table_copy[figure[0]+1][col1].lower() == "o" and table_copy[figure[0]+2][figure[1]-2] == "." and table_copy[figure[0]+1][col2]=="o":
                                row = figure[0]+1
                                table_copy[row][col1] = "."
                                table_copy[row][col2] = "."
                    if figure[1] - move[1] == -4: # double jump right
                        col1 = figure[1] + 1
                        col2 = figure[1] + 3
                        if figure[0] - 2 >= 0:
                            if table_copy[figure[0]-1][col1].lower() == "o" and table_copy[figure[0]-2][figure[1]-2] == "." and table_copy[figure[0]-1][col2]=="o":
                                row = figure[0] -1
                                table_copy[row][col1] = "."
                                table_copy[row][col2] = "."
                        if figure[0] + 2 < 8:
                            if table_copy[figure[0]+1][col1].lower() == "o" and table_copy[figure[0]+2][figure[1]-2] == "." and table_copy[figure[0]+1][col2]=="o":
                                row = figure[0]+1
                                table_copy[row][col1] = "."
                                table_copy[row][col2] = "."

            if figure_type == "o" or figure_type == "O":
                if move[0] == 7:  
                    table_copy[figure[0]][figure[1]] = "O"
                if figure[0] - move[0] == 2 or figure[0] - move[0] == -2:
                    row = figure[0] + (move[0] - figure[0]) // 2
                    column = figure[1] + (move[1] - figure[1]) // 2
                    table_copy[row][column] = "."

                if figure[0] - move[0] == 4: # double jump up
                    row1 = figure[0] - 1
                    row2 = figure[0] - 3
                    if figure[1] - move[1] == 0: # ziczac 
                        if figure[1] + 2 < 8: # right first
                            if table_copy[figure[0]-2][figure[1]+2] == "." and table_copy[figure[0]-1][figure[1]+1].lower() == "x":
                                col = figure[1] + 1
                                table_copy[row1][col] = "."
                                table_copy[row2][col] = "."
                        if figure[1] - 2 >= 0: # left first
                            if table_copy[figure[0]-2][figure[1]-2] == "." and table_copy[figure[0]-1][figure[1]-1].lower() == "x":
                                col = figure[1] - 1
                                table_copy[row1][col] = "."
                                table_copy[row2][col] = "."

                    elif figure[1] - move[1] == 4: # left double jump
                        col1 = figure[1] - 1
                        col2 = figure[1] - 3
                        table_copy[row1][col1] = "."
                        table_copy[row2][col2] = "."

                    elif figure[1] - move[1] == -4: # right double jump
                        col1 = figure[1] + 1
                        col2 = figure[1] + 3
                        table_copy[row1][col1] = "."
                        table_copy[row2][col2] = "."

                elif figure[0] - move[0] == -4: # double jump down
                    row1 = figure[0] + 1
                    row2 = figure[0] + 3
                    if figure[1] - move[1] == 0: # ziczac
                        if figure[1] + 2 < 8: # right first
                            if table_copy[figure[0]+2][figure[1]+2] == "." and table_copy[figure[0]+1][figure[1]+1].lower() == "x" and table_copy[figure[0]+3][figure[1]+1].lower() == "x":
                                
                                col = figure[1] + 1
                                table_copy[row1][col] = "."
                                table_copy[row2][col] = "."
                        if figure[1] - 2 >= 0: # left first
                            if table_copy[figure[0]+2][figure[1]-2] == "." and table_copy[figure[0]+1][figure[1]-1].lower() == "x" and table_copy[figure[0]+3][figure[1] -1].lower() == "x":
                                col = figure[1] - 1
                                table_copy[row1][col] = "."
                                table_copy[row2][col] = "."

                    elif figure[1] - move[1] == 4: # left double jump
                        col1 = figure[1] - 1
                        col2 = figure[1] - 3
                        table_copy[row1][col1] = "."
                        table_copy[row2][col2] = "."

                    elif figure[1] - move[1] == -4: # right double jump
                        col1 = figure[1] + 1
                        col2 = figure[1] + 3
                        table_copy[row1][col1] = "."
                        table_copy[row2][col2] = "."

                if figure[0] - move[0] == 0:
                    if figure[1] - move[1] == 4: # double jump left
                        col1 = figure[1] - 1
                        col2 = figure[1] - 3
                        if figure[0] - 2 >= 0:
                            if table_copy[figure[0]-1][col1].lower() == "x" and table_copy[figure[0]-2][figure[1]-2] == "." and table_copy[figure[0]-1][col2]=="x":
                                row = figure[0] -1
                                table_copy[row][col1] = "."
                                table_copy[row][col2] = "."
                        if figure[0] + 2 < 8:
                            if table_copy[figure[0]+1][col1].lower() == "x" and table_copy[figure[0]+2][figure[1]-2] == "." and table_copy[figure[0]+1][col2]=="x":
                                row = figure[0]+1
                                table_copy[row][col1] = "."
                                table_copy[row][col2] = "."
                    if figure[1] - move[1] == -4: # double jump right
                        col1 = figure[1] + 1
                        col2 = figure[1] + 3
                        if figure[0] - 2 >= 0:
                            if table_copy[figure[0]-1][col1].lower() == "x" and table_copy[figure[0]-2][figure[1]-2] == "." and table_copy[figure[0]-1][col2]=="x":
                                row = figure[0] -1
                                table_copy[row][col1] = "."
                                table_copy[row][col2] = "."
                        if figure[0] + 2 < 8:
                            if table_copy[figure[0]+1][col1].lower() == "x" and table_copy[figure[0]+2][figure[1]-2] == "." and table_copy[figure[0]+1][col2]=="x":
                                row = figure[0]+1
                                table_copy[row][col1] = "."
                                table_copy[row][col2] = "."

        table_copy[figure[0]][figure[1]], table_copy[move[0]][move[1]] = table_copy[move[0]][move[1]], table_copy[figure[0]][figure[1]]

        return table_copy

    def play_move(self, figure, move):
        table = self.generate_new_state(figure, move)
        position = None
        for state in self.get_next_moves():
            if table == state.get_table():
                position = state
                break
        return position

    def find_valid_moves_for_piece(self, coord, forced=False):
        captures = []
        valid_moves = []
        # previously checked whether the figure is valid
        figure = self._table[coord[0]][coord[1]]
        if figure != "x": # X, O, o
            if 0 <= coord[0] < 7: # not last row
                if (coord[1] - 1) >= 0: # not first col
                    if self._table[coord[0] + 1][coord[1] - 1] == '.': # left down diagonal
                        valid_moves.append((coord[0] + 1, coord[1] - 1))
                    # capture figure
                    elif coord[0] + 2 < 8 and coord[1] - 2 >= 0:
                        if self._table[coord[0] + 2][coord[1] - 2] == '.':
                            if figure.lower() != self._table[coord[0] + 1][coord[1] - 1].lower():
                                captures.append((coord[0] + 2, coord[1] - 2))
                                if coord[0] + 2 + 1 < 8 and coord[1] -2 + 1 < 8: # left right
                                    if self._table[coord[0] + 2 + 1][coord[1] -2 + 1].lower() != figure.lower() and self._table[coord[0] + 2 + 1][coord[1] -2 + 1] != ".":
                                        if (coord[0] + 2 + 2 < 8) and (coord[1] - 2 + 2 < 8):
                                            if self._table[coord[0] + 2 + 2][coord[1] - 2 + 2] == ".": 
                                                captures.append((coord[0] + 2 + 2, coord[1] - 2 + 2))
                                if coord[0] + 2 + 1 < 8 and coord[1] -2 - 1 >= 0: # left left
                                    if self._table[coord[0] + 2 + 1][coord[1] -2 - 1].lower() != figure.lower() and self._table[coord[0] + 2 + 1][coord[1] -2 - 1] != ".":
                                        if (coord[0] + 2 + 2 < 8) and (coord[1] - 2 - 2 >= 0):
                                            if self._table[coord[0] + 2 + 2][coord[1] - 2 - 2] == ".":
                                                captures.append((coord[0] + 2 + 2, coord[1] - 2 - 2))
                                if figure == "X" or figure == "O":
                                    if coord[1] - 2 - 1 >= 0: # left down up ziczac
                                        if self._table[coord[0]+1][coord[1]-2-1].lower() != figure.lower() and self._table[coord[0]+1][coord[1]-2-1] != ".":
                                            if coord[1] - 4 >= 0:
                                                if self._table[coord[0]][coord[1]-4] == ".":
                                                    captures.append((coord[0], coord[1]-4))
                             

                if (coord[1] + 1) < 8: # not last col
                    if self._table[coord[0] + 1][coord[1] + 1] == '.': # right down diagonal
                        valid_moves.append((coord[0] + 1, coord[1] + 1))
                    # capture figure
                    elif coord[0] + 2 < 8 and coord[1] + 2 < 8:
                        if self._table[coord[0] + 2][coord[1] + 2] == '.':
                            if figure.lower() != self._table[coord[0] + 1][coord[1] + 1].lower():
                                captures.append((coord[0] + 2, coord[1] + 2))
                                if coord[0] + 2 + 1 < 8 and coord[1] +2 + 1 < 8: # right right
                                    if self._table[coord[0] + 2 + 1][coord[1] +2 + 1].lower() != figure.lower() and self._table[coord[0] + 2 + 1][coord[1] +2 + 1] != ".":
                                        if (coord[0] + 2 + 2 < 8) and (coord[1] + 2 + 2 < 8):
                                            if self._table[coord[0] + 2 + 2][coord[1] + 2 + 2] == ".":
                                                captures.append((coord[0] + 2 + 2, coord[1] + 2 + 2))
                                if coord[0] + 2 +1 < 8 and coord[1] +2 -1 >= 0: # right left 
                                    if self._table[coord[0] + 2 + 1][coord[1] +2 - 1].lower() != figure.lower() and self._table[coord[0] + 2 + 1][coord[1] +2 - 1] != ".":
                                        if (coord[0] + 2 + 2 < 8) and (coord[1] + 2 - 2 >= 0):
                                            if self._table[coord[0] + 2 + 2][coord[1] + 2 - 2] == ".":
                                                captures.append((coord[0] + 2 + 2, coord[1] + 2 - 2)) 
                                if figure == "X" or figure == "O":
                                    if coord[1] + 2 + 1 < 8: # right down up ziczac
                                        if self._table[coord[0]+1][coord[1]+2+1].lower() != figure.lower() and self._table[coord[0]+1][coord[1]+2+1] != ".":
                                            if coord[1] + 4 < 8:
                                                if self._table[coord[0]][coord[1] + 4] == ".":
                                                    captures.append((coord[0], coord[1]+4))
                             
                             

        if figure != "o": # x, X, O
            if 0 < coord[0] < 8: # not first row
                if (coord[1] - 1) >= 0: # not first col
                    if self._table[coord[0] - 1][coord[1] - 1] == '.': # left up diagonal
                        valid_moves.append((coord[0] - 1, coord[1] - 1))
                    # capture figure
                    elif coord[0] - 2 >= 0 and coord[1] - 2 >= 0:
                        if self._table[coord[0] - 2][coord[1] - 2] == '.': 
                            if figure.lower() != self._table[coord[0] - 1][coord[1] - 1].lower():
                                captures.append((coord[0] - 2, coord[1] - 2))
                                if coord[0] - 2 - 1 >= 0 and coord[1] - 2 + 1 < 8: # left right
                                    if self._table[coord[0] - 2 - 1][coord[1] - 2 + 1].lower() != figure.lower() and self._table[coord[0] - 2 - 1][coord[1] - 2 + 1] != ".":
                                        if (coord[0] - 2 - 2 >= 0) and (coord[1] - 2 + 2 < 8):
                                            if self._table[coord[0] - 2 - 2][coord[1] - 2 + 2] == ".":
                                                captures.append((coord[0] - 2 - 2, coord[1] - 2 + 2))
                                if coord[0] - 2 - 1 >= 0 and coord[1] -2 -1 >= 0: # left left
                                    if self._table[coord[0] - 2 - 1][coord[1] -2 -1].lower() != figure.lower() and self._table[coord[0] - 2 - 1][coord[1] -2 -1] != ".":
                                        if (coord[0] - 2 - 2 >= 0) and (coord[1] - 2 - 2 >= 0):
                                            if (coord[0] - 2 - 2 >= 0) and (coord[1] - 2 - 2 >= 0):
                                                if self._table[coord[0] - 2 - 2][coord[1] - 2 - 2] == ".":
                                                    captures.append((coord[0] - 2 - 2, coord[1] - 2 - 2)) 
                                if figure == "X" or figure == "O":
                                    if coord[1] - 2 - 1 >= 0: # left up down ziczac
                                        if self._table[coord[0]-1][coord[1]-2-1].lower() != figure.lower() and self._table[coord[0]-1][coord[1]-2-1] != ".":
                                            if coord[1] - 4 >= 0:
                                                if self._table[coord[0]][coord[1] - 4] == ".":
                                                    captures.append((coord[0], coord[1]-4))

                if (coord[1] + 1) < 8: # not last col
                    if self._table[coord[0] - 1][coord[1] + 1] == '.':  # right up diagonal
                        valid_moves.append((coord[0] - 1, coord[1] + 1))
                    # capture figure
                    elif coord[0] - 2 >= 0 and coord[1] + 2 < 8:
                        if self._table[coord[0] - 2][coord[1] + 2] == '.':
                            if figure.lower() != self._table[coord[0] - 1][coord[1] + 1].lower():
                                captures.append((coord[0] - 2, coord[1] + 2))
                                if coord[0] - 2 - 1 >= 0 and coord[1] + 2 + 1 < 8: # right right
                                    if self._table[coord[0] - 2 - 1][coord[1] + 2 + 1].lower() != figure.lower() and self._table[coord[0] - 2 - 1][coord[1] + 2 + 1] != ".":
                                        if (coord[0] - 2 - 2 >= 0) and (coord[1] + 2 + 2 < 8):
                                            if self._table[coord[0] - 2 - 2][coord[1] + 2 + 2] == ".":
                                                captures.append((coord[0] - 2 - 2, coord[1] + 2 + 2))
                                if coord[0] - 2 - 1 >= 0 and coord[1] + 2 -1 >= 0: # right left
                                    if self._table[coord[0] - 2 - 1][coord[1] + 2 -1].lower() != figure.lower() and self._table[coord[0] - 2 - 1][coord[1] + 2 -1] != ".":
                                        if (coord[0] - 2 - 2 >= 0) and (coord[1] + 2 - 2 >= 0):
                                            if (coord[0] - 2 - 2 >= 0) and (coord[1] + 2 - 2 >= 0):
                                                if self._table[coord[0] - 2 - 2][coord[1] + 2 - 2] == ".":
                                                    captures.append((coord[0] - 2 - 2, coord[1] + 2 - 2)) 
                                if figure == "X" or figure == "O":
                                    if coord[1] + 2 + 1 < 8: # right up down ziczac
                                        if self._table[coord[0]-1][coord[1]+2+1].lower() != figure.lower() and self._table[coord[0]-1][coord[1]+2+1] != ".":
                                            if coord[1] + 4 < 8:
                                                if self._table[coord[0]][coord[1] + 2 + 2] == ".":
                                                    captures.append((coord[0], coord[1]+4))

        if forced and len(captures) != 0:
            return captures
        return captures + valid_moves
