from game import *
from  data_format import formatted_data, OUTCOME

BASIC_MOVES = ('right', 'down')
OTHER_MOVES = ('left', 'up')

def do_move(direction, curr_state, score):
    old_grid = cp.deepcopy(curr_state)
    old_score = score
    curr_state, score = play_2048(curr_state, direction, score)
    if not np.array_equal(curr_state, old_grid):
        return True, curr_state, score
    return False, old_grid, old_score

def run_rightdown(TURN_LIMIT: int = 1_000) -> (formatted_data, np.array):
    grid, score = new_game()
    result_data = formatted_data()
    turn: int = 0
    while turn < TURN_LIMIT:
        turn += 1
        try:
            valid = False
            for j in range(2):
                valid, grid, score = do_move(BASIC_MOVES[(j + turn) % 2], grid, score)
                if valid:
                    result_data.DirectionsUsed[BASIC_MOVES[(j + turn) % 2]] += 1
                    break
            if valid:
                continue
            for j in range(2):
                valid, grid, score = do_move(OTHER_MOVES[j], grid, score)
                if valid:
                    result_data.DirectionsUsed[OTHER_MOVES[j]] += 1
                    break
        except RuntimeError as inst:
            if str(inst)== "GO":
                print("GAME OVER in ", turn, " moves")
                result_data.Outcome = OUTCOME.Loss
            elif str(inst)== "WIN":
                print("WIN in ", turn, " moves")
                result_data.Outcome = OUTCOME.Win
            break
    # print_grid(grid, score)
    result_data.Score = score
    result_data.NumTurns = turn
    return result_data, grid

# Best solution found in 332 turns
# outcome: 0
# Score:  4120
# +----+----+----+----+
# |   2|   4|   2|   8|
# +----+----+----+----+
# |   4|   8|  32|   2|
# +----+----+----+----+
# |   2|   4|  64| 128|
# +----+----+----+----+
# |  32|  64| 128| 256|
# +----+----+----+----+
#
# Worst solution found in 89 turns
# outcome: 0
# Score:  660
# +----+----+----+----+
# |   4|   2|   4|   2|
# +----+----+----+----+
# |   2|   4|   8|   4|
# +----+----+----+----+
# |   4|   8|  32|  64|
# +----+----+----+----+
# |   8|  32|   4|  16|
# +----+----+----+----+
#
# Average data
# avg score: 2320.800
# avg turns: 213.200
# avg time: 0.02s/game
#           0.00s/turn
# wins: 0, losses: 30
# not finished games: 0
# winrate (of finished games): 0.00
# winrate (of all games):      0.00
#
# Turns up: 0 (0.00%)
# Turns down: 2765 (43.23%)
# Turns right: 3116 (48.72%)
# Turns left: 485 (7.58%)