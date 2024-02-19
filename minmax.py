import numpy as np
import copy as cp
from game import *
# from fitness_function import fitness_function
from measure import measure
from data_format import formatted_data, OUTCOME

MOVE_SIMULATIONS = 10
MAX_DEPTH = (3, 7)


def fitness_function(grid: np.array, score: int):
    """
    Return value of a board based on average tile value, score and number of empty tiles.

    :param grid: 2D array representing the 2048 board
    :param score: Value of the in-game score
    :return: evaluation of board
    """
    return np.sum(grid) / np.count_nonzero(grid) + score + np.size(grid[grid == 0])



def take_move(grid, score, move):
    """
    Take a move in corresponding direction without spawning a new tile.

    :param grid: 2D array representing the 2048 board
    :param score: Value of the in-game score
    :param move: Direction which way should the board be moved
    :return: New board and new score 
    """
    if move == 'left':
        grid, score = move_left(grid, score)
    elif move == 'right':
        grid, score = move_right(grid, score)
    elif move == 'up':
        grid, score = move_up(grid, score)
    elif move == 'down':
        grid, score = move_down(grid, score)
    else:
        raise ValueError("Invalid move")
    return grid, score


def minimax(grid, score, depth, is_maximizing: bool, alpha = -np.inf, beta = np.inf) -> (float, str):
    """
    Recursive minimax to evaluating the state of board based on it's children.

    :param grid: 2D array representing the 2048 board
    :param score: Value of the in-game score
    :param depth: Maximum value of recursion
    :param is_maximizing: Who is playing - true = player; false = game (spawning a tile)
    :param alpha: Best value that can a Maximizing player get in previous branches
    :param beta: Best value that can a Minimizing player get in previous branches
    :param move: Direction which way should the board be moved
    :return: Best value that could be gained and string of a move direction to get it
    """
    if check_game_over(grid):
        return 0.5 * fitness_function(grid, score), ''
    elif check_win(grid):
        return np.inf, ''
    elif depth == 0:
        return fitness_function(grid, score), ''

    # Player turn
    if is_maximizing:
        maxVal = -np.inf
        best_move: str = ''
        for move in MOVES:
            # Take a move without generating new tile
            new_grid, new_score = take_move(cp.deepcopy(grid), score, move)
            # If the move isn't legal, don't continue with this branch
            if np.array_equal(new_grid, grid):
                continue

            # Get the worst possible outcome after this move
            val, _ = minimax(new_grid, new_score, depth-1, False, alpha, beta)
            if val > maxVal:
                maxVal = val
                best_move = move

            # alpha beta pruning
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return maxVal, best_move

    # Game turn - generating tile
    minVal = np.inf
    for _ in range(MOVE_SIMULATIONS):
        # Generate a new tile 
        new_grid = cp.deepcopy(grid)
        board_full = not add_new_number(new_grid)
        val, _ = minimax(new_grid, score, depth-1, True, alpha, beta)
        minVal = min(val, minVal)

        # alpha beta pruning
        beta = min(beta, val)
        if beta <= alpha:
            break

        # If the board was full, don't make more simulations 
        if board_full:
            break
    return  minVal, ''



def run_minmax(TURN_LIMIT: int = 1_000) -> (formatted_data, np.array):
    """
    Fully plays a game of 2048 by using Minimax algorithm.
    
    :param TURN_LIMIT: Maximum number of turns ai can take
    :return: Structure with data about the game and final grid 
    """
    grid, score = new_game()
    outcome: OUTCOME = OUTCOME.NotComplete
    turn: int = 0

    depth = 0
    while turn < TURN_LIMIT:
        turn += 1


        # Set depth on higher value later in game or if getting close to filling up the board
        depth = MAX_DEPTH[0] if np.max(grid) < 1024 and np.count_nonzero(grid) < 14 else MAX_DEPTH[1]
        _, best_move = minimax(grid, score, depth, True)

        try:
            grid, score = play_2048(grid, best_move, score)
        except RuntimeError as inst:
            if str(inst) == "GO":
                outcome = OUTCOME.Loss
            elif str(inst)== "WIN":
                outcome = OUTCOME.Win
            break

    # print()
    # print_grid(grid, score)
    return formatted_data(
        score=score,
        outcome=outcome,
        num_turns=turn
    ), grid

if __name__ == '__main__':
    print("MINMAX METHOD")
    measure(run_minmax, 1000, 30)


# Best solution found in 975 turns
# outcome: OUTCOME.Win
# Score:  18324
# +----+----+----+----+
# |    |    |    |   2|
# +----+----+----+----+
# |    |    |    |    |
# +----+----+----+----+
# |    |    |  16|2048|
# +----+----+----+----+
# |   2|  32|  16|   4|
# +----+----+----+----+
#
# Average data
# avg score: 13931.47
# avg turns: 810.17
# avg time: 152.35s/game
#           0.19s/turn
# wins/finished: 8/30 = 0.267
