from game import *
import copy as cp
import numpy as np
# from fitness_function import fitness_function
from measure import measure
from data_format import formatted_data, OUTCOME

NUM_SIMULATIONS = 20
SIMULATION_DEPTH = 100


def fitness_function(grid: np.array, score: int):
    """
    Return value of a board based on average tile value and score.

    :param grid: 2D array representing the 2048 board
    :param score: Value of the ingame score
    :return: evaluation of board
    """
    return pow(np.sum(grid) / np.count_nonzero(grid), 4) + score


def do_random_turn(grid, score):
    """
    Take a random legal move and return new position of board and score.

    :param grid: 2D array representing the 2048 board
    :param score: Value of the ingame score
    :return: New board and new score 
    """
    new_grid = cp.deepcopy(grid)
    new_score = score
    while np.array_equal(new_grid, grid):
        direction = np.random.choice(MOVES)
        new_grid, new_score = play_2048(new_grid, direction, score)
    return new_grid, new_score


def run_simulations(grid, score, depth):
    """
    Take a depth number of random turnes, evaluate board after the final one. 
    When reaching end-state (win or loss), return fitness of the end-state board.

    :param grid: 2D array representing the 2048 board
    :param score: Value of the ingame score
    :param depth: Number of random turns to take
    :return: Fitness of board after last move of simulation
    """
    num_of_wins = 0
    new_score = 0
    new_grid = cp.deepcopy(grid)
    for _ in range(depth):
        try:
            new_grid, new_score = do_random_turn(new_grid, score)
        except RuntimeError as inst:
            if str(inst) == "GO":
                return 0.1 * fitness_function(new_grid, new_score)
            elif str(inst) == "WIN":
                return 100 * fitness_function(new_grid, new_score)

    return fitness_function(new_grid, new_score)


def run_montecarlo(TURN_LIMIT: int = 1_000):
    """
    Fully playes a game of 2048 by using Monte Carlo Simulation.
    
    :param TURN_LIMIT: Maximum number of turns AI can take
    :return: Structure with data about the game and final grid
    """
    grid, score = new_game()
    result_data = formatted_data()
    turn: int = 0

    while turn < TURN_LIMIT:
        if check_game_over(grid):
            result_data.Outcome = OUTCOME.Loss
            break

        turn += 1

        # figure out best move
        best_move = ''
        best_fitness = -np.inf
        for move in MOVES:
            sims_fitness: np.float = 0
            try:
                for i in range(NUM_SIMULATIONS):
                    # do first initial move
                    next_grid, next_score = play_2048(cp.deepcopy(grid), move, score)
                    if np.array_equal(next_grid, grid):
                        sims_fitness = -np.inf
                        break

                    # simulation of taking N random moves after initial move
                    sims_fitness += run_simulations(next_grid, next_score, SIMULATION_DEPTH) / NUM_SIMULATIONS
            except RuntimeError as inst:
                if str(inst) == "GO":
                    break
                elif str(inst) == "WIN":
                    # If the initial move is winning set it as best move and return formatted_data 
                    best_move = move
                    break

            # update best_move if this simulation had better result
            if sims_fitness > best_fitness:
                best_move = move
                best_fitness = sims_fitness

        # take a turn according to best move
        try:
            if not best_move in MOVES:
                raise ValueError('Invalid Move')

            grid, score = play_2048(grid, best_move, score)
            result_data.DirectionsUsed[best_move] += 1
        except RuntimeError as inst:
            if str(inst) == "GO":
                result_data.Outcome = OUTCOME.Loss
            elif str(inst) == "WIN":
                result_data.Outcome = OUTCOME.Win
            break

    result_data.Score = score
    result_data.NumTurns = turn
    return result_data, grid


if __name__ == '__main__':
    print("MONTE CARLO METHOD")
    measure(run_montecarlo, 1000, 30)


# Best solution found in 985 turns
# outcome: OUTCOME.Win
# Score:  18364
# +----+----+----+----+
# |    |   2|    |    |
# +----+----+----+----+
# |   2|   4|    |   4|
# +----+----+----+----+
# |  16|  32|   4|  16|
# +----+----+----+----+
# |   2|  16|2048|   4|
# +----+----+----+----+
#
# Average data
# avg score: 14872.0
# avg turns: 841.2333333333333
# avg time: 193.27s/game
#           0.23s/turn
# wins/finished: 11/30 = 0.367
