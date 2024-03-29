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

# -------------------------------
# Best solution found in 337 turns
# outcome: 0
# Score:  4116
# +----+----+----+----+
# |   2|   4|   8|   2|
# +----+----+----+----+
# |   4|   8|   2|  32|
# +----+----+----+----+
# |   8|  16|  64| 128|
# +----+----+----+----+
# |  16|  64| 128| 256|
# +----+----+----+----+
# Turns up: 0 (0.00%)
# Turns down: 145 (43.03%)
# Turns right: 155 (45.99%)
# Turns left: 36 (10.68%)
#
# Worst solution found in 93 turns
# outcome: 0
# Score:  668
# +----+----+----+----+
# |   2|   4|   8|   2|
# +----+----+----+----+
# |   4|   8|   4|  16|
# +----+----+----+----+
# |   8|  16|  64|   2|
# +----+----+----+----+
# |  16|  32|   4|  16|
# +----+----+----+----+
# Turns up: 0 (0.00%)
# Turns down: 40 (43.01%)
# Turns right: 43 (46.24%)
# Turns left: 9 (9.68%)
#
# Average data
# avg score: 2185.733
# avg turns: 202.667 (6080)
# avg time: 0.04s/game
#           0.00s/turn
# wins: 0, losses: 30
# not finished games: 0
# winrate (of finished games): 0.00
# winrate (of all games):      0.00
#
# Turns up: 0 (0.00%)
# Turns down: 2654 (43.65%)
# Turns right: 2923 (48.08%)
# Turns left: 473 (7.78%)