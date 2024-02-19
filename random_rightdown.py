from game import *

BASIC_MOVES = ('right', 'down')
OTHER_MOVES = ('left', 'up')

def do_move(direction, curr_state, score):
    old_grid = cp.deepcopy(curr_state)
    old_score = score
    curr_state, score = play_2048(curr_state, direction, score)
    if not np.array_equal(curr_state, old_grid):
        return True, curr_state, score
    return False, old_grid, old_score

def run_rightdown(TURN_LIMIT: int = 1_000):
    grid, score = new_game()
    has_win: bool = False
    turn: int = 0
    while turn < TURN_LIMIT:
        turn += 1
        try:
            valid = False
            for j in range(2):
                valid, grid, score = do_move(BASIC_MOVES[j + turn % 2], grid, score)
                if valid:
                    break
            if valid:
                continue
            for j in range(2):
                valid, grid, score = do_move(OTHER_MOVES[j], grid, score)
                if valid:
                    break

        except RuntimeError as inst:
            if str(inst)== "GO":
                print("GAME OVER in ", turn, " moves")
            elif str(inst)== "WIN":
                print("WIN in ", turn, " moves")
                has_win = True 
            break
    # print_grid(grid, score)
    return {
        "score": score,
        "has_win": has_win,
        "num_turns": turn,
    }, grid
