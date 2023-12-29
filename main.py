from input import *
from output import print_table
from heuristic import Position
from math import inf
from time import time
from copy import deepcopy
from algorithm import *


def determine_dynamic_depth(time_previous_move, depth, forced_capture, num_moves):
    """ 
    Change the depth when the runtime is too slow or too fast
    
    """
    # if forced_capture:
    #     if time_previous_move < 0.5 and num_moves <= 6:
    #         return depth + 1
    #     if depth > 6 and (time_previous_move > 4 or num_moves > 6):
    #         return depth - 1
    #     return depth
    # else:
    #     if time_previous_move < 0.5:
    #         return depth + 1
    #     if time_previous_move > 4.5:
    #         return depth - 1
    #     return depth
    return depth

def ending_conditions(position, figure_counter, forced_capture):
    moves = position.get_next_moves(forced_capture)
    num_figures = position.count_pieces()
    if num_figures[0] == 0:
        print("Black won!")
        return True
    if num_figures[1] == 0:
        print("White won!")
        return True
    if num_figures[0] + num_figures[1] == figure_counter[0]:
        figure_counter[1] += 1
        if figure_counter[1] == 50:
            if num_figures[0] > num_figures[1]:
                print("White won!", num_figures[0], "vs", num_figures[1])
            elif num_figures[0] < num_figures[1]:
                print("Black won!", num_figures[1], "vs", num_figures[0])
            else:
                print("Tie!")
            return True
    else:
        figure_counter[0] = num_figures[0] + num_figures[1]
        figure_counter[1] = 0
    if not moves:
        print("There are no possible moves left! Game is finished!")
        return True
    return False

res = [] # store runtime for each AI move
def main():
    """
    Main function to run the game

    """
    table = [['.', 'o', '.', "o", '.', "o", '.', "o"],
             ["o", '.', "o", '.', "o", '.', "o", '.'],
             ['.', "o", '.', "o", '.', "o", '.', "o"],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ["x", '.', "x", '.', "x", '.', "x", '.'],
             ['.', "x", '.', "x", '.', "x", '.', "x"],
             ["x", '.', "x", '.', "x", '.', "x", '.']]

    forced_capture = input_forced_moves()

    position = Position(table, False)
    time_previous_move = 4.5
    depth = 6

    # the number of figures, and a counter of how many moves have passed without capturing
    without_capture = [0, 0]

    while True:
        if ending_conditions(position, without_capture, forced_capture):
            break
        if position._white_to_move:
#             num_moves_white = len(position.get_next_moves())
#             depth = determine_dynamic_depth(time_previous_move, depth, forced_capture, num_moves_white)
#             previous_table = deepcopy(position.get_table())

#             print("Player1 thinking...............................")
#             print("New depth is {} ".format(depth))

#             t1 = time()
#             num_figures = position.count_pieces()
#             if num_figures[0] + num_figures[1] > 6:
#                 alpha_beta(position, depth, -inf, inf, False, forced_capture)
#                 #min_max(position, depth, False, forced_capture)
#                 position = min(position.get_next_moves())
#             else:
#                 alpha_beta(position, 10, -inf, inf, False, forced_capture)
#                 #min_max(position, 15, False, forced_capture)
#                 position = min(position.get_next_moves())
#             # alpha_beta(position, depth, -inf, inf, False, forced_capture)
#             # position = min(position.get_next_moves())
#             t2 = time()
#             time_previous_move = t2 - t1

#             #res.append(time_previous_move) # store AI process time in res
    
#             differences = position.find_move_played(previous_table)
#             print(time_previous_move)
#             print_table(position.get_table(), differences) # print the move played by the AI
#             print("Player1 played a move displayed on the table above.\n\n")

            available_pieces = position.find_capturing_moves()
            if forced_capture:
                print_table(position.get_table(), available_pieces)
                piece = input_choose_piece(position, available_pieces)
            else:
                print_table(position.get_table())
                piece = input_choose_piece(position)

            if not piece:
                print("Goodbye! See you again!")
                break

            valid_moves = position.find_valid_moves_for_piece(piece, forced_capture)
            print_table(position.get_table(), piece, valid_moves)
            new_position = input_choose_field(valid_moves)
            if not new_position:
                print("Goodbye!")
                break

            previous_table = deepcopy(position.get_table())
            position = position.play_move(piece, new_position)
            differences = position.find_move_played(previous_table)
            
            print("User played the move displayed on the table above.\n\n\n")

        if ending_conditions(position, without_capture, forced_capture):
            break
        # available_pieces = position.find_capturing_moves()
        # if forced_capture:
        #     print_table(position.get_table(), available_pieces)
        #     piece = input_choose_piece(position, available_pieces)
        # else:
        #     print_table(position.get_table())
        #     piece = input_choose_piece(position)

        # if not piece:
        #     print("Goodbye! Never see you again!")
        #     break

        # valid_moves = position.find_valid_moves_for_piece(piece, forced_capture)
        # print_table(position.get_table(), piece, valid_moves)
        # new_position = input_choose_field(valid_moves)
        # if not new_position:
        #     print("Goodbye!")
        #     break

        # previous_table = deepcopy(position.get_table())
        # position = position.play_move(piece, new_position)
        # differences = position.find_move_played(previous_table)
        
        # print("User played the move displayed on the table above.\n\n\n")
        if not position._white_to_move:
            num_moves = len(position.get_next_moves())
            depth = determine_dynamic_depth(time_previous_move, depth, forced_capture, num_moves)
            previous_table = deepcopy(position.get_table())

            print("COM PROCESSING.....................................")
            print("New depth is {} ".format(depth))
            
            t3 = time()
            num_figures = position.count_pieces()
            if num_figures[0] + num_figures[1] > 7:
                alpha_beta_max(position, depth, -inf, inf, True, forced_capture)
                #min_max(position, depth, True, forced_capture)
                position = max(position.get_next_moves())
            else:
                alpha_beta_ending(position, 10, -inf, inf, True, forced_capture)
                #min_max(position, 15, True, forced_capture)
                position = max(position.get_next_moves())
            # alpha_beta_ending(position, depth, -inf, inf, True, forced_capture)
            # #min_max(position, 15, True, forced_capture)
            # position = max(position.get_next_moves())
            t4 = time()
            time_previous_move = t4 - t3

            res.append(time_previous_move) # store AI process time in res
    
            differences = position.find_move_played(previous_table)
            print(time_previous_move)
            print_table(position.get_table(), differences) # print the move played by the AI
            print("COM played a move displayed on the table above.\n\n")
    
    # Store runtime in text file for later calculation
    file = "test.txt"
    with open(file, 'a') as f:
        f.write(str(res) + "\n")

if __name__ == '__main__':
    main()
