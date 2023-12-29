from math import inf
import random

# random implementation
def random_move(valid_moves):
    moves = random.shuffle(valid_moves)
    return random.choice(moves)

# MIN MAX simple implementation

def min_max(position, depth, max_player, forced_capture):
    if depth == 0 or position.get_game_end():
        return position.evaluate_state()
    if max_player:
        max_evaluation = -inf
        for child in position.get_next_moves(forced_capture):
            eval = min_max(child, depth - 1, False, forced_capture)
            max_evaluation = max(max_evaluation, eval)
        position.set_evaluation(max_evaluation)
        return max_evaluation
    else:
        min_evaluation = inf
        for child in position.get_next_moves(forced_capture):
            eval = min_max(child, depth - 1, True, forced_capture)
            min_evaluation = min(min_evaluation, eval)
        position.set_evaluation(min_evaluation)
        return min_evaluation

# MIN MAX with ALPHA-BETA pruning

def alpha_beta(position, depth, alpha, beta, max_player, forced_capture):
    if depth == 0 or position.get_game_end():
        return position.evaluate_state()
    if max_player:
        max_evaluation = -inf
        for child in position.get_next_moves(forced_capture):
            eval = alpha_beta(child, depth - 1, alpha,
                              beta, False, forced_capture)
            max_evaluation = max(max_evaluation, eval)
            alpha = max(alpha, eval)
            if beta <= alpha: # prune
                # print("pruning max")
                break
        position.set_evaluation(max_evaluation)
        return max_evaluation
    else:
        min_evaluation = inf
        for child in position.get_next_moves(forced_capture):
            eval = alpha_beta(child, depth - 1, alpha,
                              beta, True, forced_capture)
            min_evaluation = min(min_evaluation, eval)
            beta = min(beta, eval)
            if beta <= alpha: # prune
                # print("pruning min")
                break
        position.set_evaluation(min_evaluation)
        return min_evaluation


# Alpha beta pruning minmax that calls a different heuristics function. It can be changed to take the function as a parameter

def alpha_beta_ending(position, depth, alpha, beta, max_player, forced_capture):
    if depth == 0 or position.get_game_end():
        return position.evaluate_state_ending()
    if max_player:
        max_evaluation = -inf
        for child in position.get_next_moves(forced_capture):
            eval = alpha_beta_ending(child, depth - 1, alpha, beta, False, forced_capture)
            max_evaluation = max(max_evaluation, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                # print("pruning max")
                break
        position.set_evaluation(max_evaluation)
        return max_evaluation
    else:
        min_evaluation = inf
        for child in position.get_next_moves(forced_capture):
            eval = alpha_beta_ending(child, depth - 1, alpha, beta, True, forced_capture)
            min_evaluation = min(min_evaluation, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                # print("pruning min")
                break
        position.set_evaluation(min_evaluation)
        return min_evaluation

# AB pruning with best heuristic available

def alpha_beta_max(position, depth, alpha, beta, max_player, forced_capture):
    if depth == 0 or position.get_game_end():
        return position.heuristic()
    if max_player:
        max_evaluation = -inf
        for child in position.get_next_moves(forced_capture):
            eval = alpha_beta_max(child, depth - 1, alpha, beta, False, forced_capture)
            max_evaluation = max(max_evaluation, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                # print("pruning max")
                break
        position.set_evaluation(max_evaluation)
        return max_evaluation
    else:
        min_evaluation = inf
        for child in position.get_next_moves(forced_capture):
            eval = alpha_beta_max(child, depth - 1, alpha, beta, True, forced_capture)
            min_evaluation = min(min_evaluation, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                # print("pruning min")
                break
        position.set_evaluation(min_evaluation)
        return min_evaluation